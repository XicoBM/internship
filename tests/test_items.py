from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json())


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    client.post("/items", json={"name": "Item500000", "price": 1})
    response = client.get("/items")
    names = [item["name"] for item in response.json()]
    assert "Item500000" in names

def test_neg_price_item() -> None:
    response = client.post("/items", json={"name": "Item500000", "price": -1})
    assert response.status_code == 422
    
def test_inexistent_item_update() -> None:
    response = client.put("/items/10000000", json={"name": "NewName"})
    assert response.status_code == 400
    
def test_partial_update() -> None:
    unique_name = "ItemPartialUpdateTest"
    client.post("/items", json={"name": unique_name, "price": 1})
    id = [item["id"] for item in client.get("/items").json() if item["name"] == unique_name][0]
    response = client.put(f"/items/{id}", json={"name": "NewName"})
    assert response.status_code == 200
    assert response.json() == {"id": id, "name": "NewName", "price": 1}
    
def test_update_item_name() -> None:
    client.post("/items", json={"name": "ItemToUpdate", "price": 1})
    id = [item["id"] for item in client.get("/items").json() if item["name"] == "ItemToUpdate"][0]
    response = client.put(f"/items/{id}", json={"name": "ab"})
    assert response.status_code == 422