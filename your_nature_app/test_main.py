import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from your_nature_app.main import app, get_db
from your_nature_app.tables.products import Base

client = TestClient(app)
HTTP_OK = 200
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def _override_get_db(test_db) -> None:
    app.dependency_overrides[get_db] = lambda: test_db
    yield
    del app.dependency_overrides[get_db]


def test_add_molecule(_override_get_db):
    product_data = {"name": "Face cream", "price": "21.99", "stock": 46}

    response = client.post("/store", json=product_data)

    assert response.status_code == 200
    client.delete("/store")


def test_add_molecules(_override_get_db):
    product_data = [
        {"name": "Face cream", "price": "20.99", "stock": 46},
        {"name": "Facial tonic", "price": "23.99", "stock": 18},
    ]

    response = client.post("/store", json=product_data)

    assert response.status_code == 200
    client.delete("/store")
