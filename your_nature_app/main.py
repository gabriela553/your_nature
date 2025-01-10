import os

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from your_nature_app.tables.products import ProductInDB
from dotenv import load_dotenv

from your_nature_app.tables.products import Base

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

app = FastAPI()


class Product(BaseModel):
    id: int | None = None
    name: str
    price: float
    stock: int

    @staticmethod
    def from_product_in_db(product_in_db: ProductInDB):
        return Product(
            id=product_in_db.id,
            name=product_in_db.name,
            price=product_in_db.price,
            stock=product_in_db.stock,
        )

    def to_product_in_db(self):
        return ProductInDB(
            id=self.id, name=self.name, price=self.price, stock=self.stock
        )


async def get_db():
    engine = create_engine(CONNECTION_STRING, echo=True)
    db = Session(engine)
    Base.metadata.create_all(engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/store")
async def add_product(products: Product | list[Product], db=Depends(get_db)):
    if isinstance(products, list):
        for product in products:
            product_db = product.to_product_in_db()
            db.add(product_db)
    else:
        product_db = products.to_product_in_db()
        db.add(product_db)
    db.commit()
