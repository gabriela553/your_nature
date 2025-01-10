from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ProductInDB(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[float]
    stock: Mapped[int]

    def __repr__(self) -> str:

        return (
            f"Product(name={self.name!r}, price={self.price!r}, stock={self.stock!r})"
        )
