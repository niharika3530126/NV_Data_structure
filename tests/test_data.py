import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app, get_db
from app.database import Base


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

def test_create_dataset(client):
    response = client.post(
        "/datasets",
        json={
            "name": "Customer",
            "description": "Customer master data",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Customer"
    assert isinstance(data["id"], int)


def test_dataset_name_must_be_unique(client):
    client.post(
        "/datasets",
        json={"name": "Order", "description": "Orders"},
    )

    response = client.post(
        "/datasets",
        json={"name": "Order", "description": "Orders"},
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_add_data_element_to_dataset(client):
    dataset_response = client.post(
        "/datasets",
        json={"name": "Product", "description": "Product data"},
    )

    dataset_id = dataset_response.json()["id"]

    element_response = client.post(
        f"/datasets/{dataset_id}/elements",
        json={
            "name": "price",
            "data_type": "float",
            "is_required": True,
            "is_pii": False,
        },
    )

    assert element_response.status_code == 200

    element = element_response.json()
    assert element["name"] == "price"
    assert element["data_type"] == "float"
    assert element["is_required"] is True
    assert element["is_pii"] is False
    assert isinstance(element["id"], int)
