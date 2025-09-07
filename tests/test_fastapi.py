import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise_fastapi_crud import TortoiseCRUDRouter, SchemaConfig
from models import Model, ItemCreate, Item, ItemSchema

# --- App Fixture ---


@pytest.fixture(scope="module")
def app() -> FastAPI:
    app = FastAPI()

    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )

    schema_cfg = SchemaConfig(
        db_model=Item,
        schema=ItemSchema,
        create_schema=ItemCreate,
        update_schema=ItemCreate,
        prefix="/items",
        tags=["Items"],
        paginate=10,
    )
    router = TortoiseCRUDRouter(schema_cfg)
    app.include_router(router)

    return app


@pytest.fixture(scope="module")
def client(app: FastAPI) -> TestClient:
    with TestClient(app) as c:
        yield c


def test_create_item(client: TestClient):
    response = client.post("/items/", json={"name": "First"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "First"


def test_get_all_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_one_item(client: TestClient):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "First"


def test_update_item(client: TestClient):
    response = client.put("/items/1", json={"name": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"


def test_delete_one_item(client: TestClient):
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_delete_all_items(client: TestClient):
    client.post("/items/", json={"name": "Second"})
    response = client.delete("/items/")
    assert response.status_code == 200
    data = response.json()
    assert data == []
