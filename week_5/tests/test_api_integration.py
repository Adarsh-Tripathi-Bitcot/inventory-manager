# # tests/test_api_integration.py
# import json
# from pathlib import Path

# import pytest

# from api.app import create_app


# @pytest.fixture
# def client(tmp_path: Path):
#     csv_file = tmp_path / "products.csv"
#     csv_file.write_text(
#         "product_id,product_name,quantity,price,type,expiry_date,warranty_period,author,pages\n"
#         "201,Strawberries,12,3.0,food,2025-10-05,,,\n"
#         "206,Smartphone,3,70000,electronic,,18,,\n"
#     )
#     app = create_app({"DATA_CSV": str(csv_file)})
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client


# def test_get_all_products(client):
#     resp = client.get("/api/products")
#     assert resp.status_code == 200
#     body = resp.get_json()
#     assert isinstance(body, list)
#     assert any(p["product_id"] == "201" for p in body)


# def test_get_product_found(client):
#     resp = client.get("/api/products/201")
#     assert resp.status_code == 200
#     body = resp.get_json()
#     assert body["product_id"] == "201"
#     assert body["product_name"] == "Strawberries"


# def test_get_product_not_found(client):
#     resp = client.get("/api/products/9999")
#     assert resp.status_code == 404


# def test_create_product_success(client):
#     new_product = {
#         "product_id": "999",
#         "product_name": "Test Book",
#         "quantity": 5,
#         "price": 10.0,
#         "type": "book",
#         "author": "Alice",
#         "pages": 123,
#     }
#     resp = client.post("/api/products", json=new_product)
#     assert resp.status_code == 201
#     body = resp.get_json()
#     assert body["product_id"] == "999"

#     # new product accessible via GET
#     resp2 = client.get("/api/products/999")
#     assert resp2.status_code == 200


# def test_create_product_conflict(client):
#     conflict = {
#         "product_id": "201",
#         "product_name": "Dup",
#         "quantity": 1,
#         "price": 1.0,
#         "type": "food",
#         "expiry_date": "2025-12-12",
#     }
#     resp = client.post("/api/products", json=conflict)
#     assert resp.status_code == 409


# def test_create_product_validation_error(client):
#     bad = {
#         "product_id": "500",
#         "product_name": "Bad Data",
#         "quantity": -4,
#         "price": -10.0,
#         "type": "food",
#     }
#     resp = client.post("/api/products", json=bad)
#     assert resp.status_code == 400


# def test_update_product_success(client):
#     update = {
#         "product_id": "201",
#         "product_name": "Strawberry (Updated)",
#         "quantity": 20,
#         "price": 4.5,
#         "type": "food",
#         "expiry_date": "2026-01-01",
#     }
#     resp = client.put("/api/products/201", json=update)
#     assert resp.status_code == 200
#     body = resp.get_json()
#     assert body["product_name"] == "Strawberry (Updated)"


# def test_update_product_not_found(client):
#     update = {
#         "product_id": "4242",
#         "product_name": "Nope",
#         "quantity": 1,
#         "price": 1.0,
#         "type": "book",
#         "author": "A",
#         "pages": 10,
#     }
#     resp = client.put("/api/products/4242", json=update)
#     assert resp.status_code == 404


# def test_delete_product_success(client):
#     # Ensure it exists first
#     resp_before = client.get("/api/products/206")
#     assert resp_before.status_code == 200

#     # Delete
#     resp = client.delete("/api/products/206")
#     assert resp.status_code == 204
#     assert resp.data == b""  # 204 should have empty body

#     # Verify it is gone
#     resp_after = client.get("/api/products/206")
#     assert resp_after.status_code == 404


# def test_delete_product_not_found(client):
#     resp = client.delete("/api/products/9999")
#     assert resp.status_code == 404
#     body = resp.get_json()
#     assert body["error"] == "Product not found"







# week_5/tests/test_api_integration.py
import json
from pathlib import Path

import pytest

from api.app import create_app


@pytest.fixture
def client(tmp_path: Path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "product_id,product_name,quantity,price,type,expiry_date,warranty_period,author,pages\n"
        "201,Strawberries,12,3.0,food,2025-10-05,,,\n"
        "206,Smartphone,3,70000,electronic,,18,,\n"
    )
    app = create_app({"DATA_CSV": str(csv_file)})
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_products(client):
    resp = client.get("/api/products")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
    assert any(p["product_id"] == "201" for p in body)


def test_get_product_found(client):
    resp = client.get("/api/products/201")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["product_id"] == "201"
    assert body["product_name"] == "Strawberries"


def test_get_product_not_found(client):
    resp = client.get("/api/products/9999")
    assert resp.status_code == 404


def test_create_product_success(client):
    new_product = {
        "product_id": "999",
        "product_name": "Test Book",
        "quantity": 5,
        "price": 10.0,
        "type": "book",
        "author": "Alice",
        "pages": 123,
    }
    resp = client.post("/api/products", json=new_product)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["product_id"] == "999"

    # new product accessible via GET
    resp2 = client.get("/api/products/999")
    assert resp2.status_code == 200


def test_create_product_conflict(client):
    conflict = {
        "product_id": "201",
        "product_name": "Dup",
        "quantity": 1,
        "price": 1.0,
        "type": "food",
        "expiry_date": "2025-12-12",
    }
    resp = client.post("/api/products", json=conflict)
    assert resp.status_code == 409


def test_create_product_validation_error(client):
    bad = {
        "product_id": "500",
        "product_name": "Bad Data",
        "quantity": -4,
        "price": -10.0,
        "type": "food",
    }
    resp = client.post("/api/products", json=bad)
    assert resp.status_code == 400


def test_create_product_missing_json(client):
    resp = client.post("/api/products", data="not json")
    assert resp.status_code == 400


def test_update_product_success(client):
    update = {
        "product_id": "201",
        "product_name": "Strawberry (Updated)",
        "quantity": 20,
        "price": 4.5,
        "type": "food",
        "expiry_date": "2026-01-01",
    }
    resp = client.put("/api/products/201", json=update)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["product_name"] == "Strawberry (Updated)"


def test_update_product_not_found(client):
    update = {
        "product_id": "4242",
        "product_name": "Nope",
        "quantity": 1,
        "price": 1.0,
        "type": "book",
        "author": "A",
        "pages": 10,
    }
    resp = client.put("/api/products/4242", json=update)
    assert resp.status_code == 404


def test_update_product_invalid_json(client):
    resp = client.put("/api/products/201", data="not json")
    assert resp.status_code == 400


def test_delete_product_success(client):
    resp_before = client.get("/api/products/206")
    assert resp_before.status_code == 200

    resp = client.delete("/api/products/206")
    assert resp.status_code == 204
    assert resp.data == b""

    resp_after = client.get("/api/products/206")
    assert resp_after.status_code == 404


def test_delete_product_not_found(client):
    resp = client.delete("/api/products/9999")
    assert resp.status_code == 404
    body = resp.get_json()
    assert body["error"] == "Product not found"


def test_row_to_model_invalid_type(client):
    # This will trigger _row_to_model returning None for invalid row
    csv_file = Path(client.application.config["DATA_CSV"])
    csv_file.write_text(
        "product_id,product_name,quantity,price,type,expiry_date,warranty_period,author,pages\n"
        "501,Bad Product,abc,xyz,unknown,,,,\n"
    )
    resp = client.get("/api/products")
    body = resp.get_json()
    # should skip invalid row
    assert all(p["product_id"] != "501" for p in body)


def test_create_product_unknown_type_defaults_generic(client):
    new_product = {
        "product_id": "888",
        "product_name": "Generic Product",
        "quantity": 1,
        "price": 1.0,
        "type": "unknown_type",
    }
    resp = client.post("/api/products", json=new_product)
    assert resp.status_code == 201
    body = resp.get_json()
    # Should be created as generic Product
    assert "product_id" in body
    assert body["product_id"] == "888"


def test_create_product_invalid_warranty_and_pages(client):
    new_product = {
        "product_id": "777",
        "product_name": "Bad Data Product",
        "quantity": 1,
        "price": 10,
        "type": "electronic",
        "warranty_period": "not_a_number",
    }
    resp = client.post("/api/products", json=new_product)
    # Should fallback to None and still create
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["product_id"] == "777"

    # Now test for book pages invalid
    new_book = {
        "product_id": "776",
        "product_name": "Bad Pages Book",
        "quantity": 1,
        "price": 5.0,
        "type": "book",
        "pages": "not_a_number",
    }
    resp2 = client.post("/api/products", json=new_book)
    assert resp2.status_code == 201
    body2 = resp2.get_json()
    assert body2["pages"] is None



def test_update_product_conflict_and_invalid_fields(client):
    # Test updating non-existent product triggers 404 already done
    # Now test invalid field types
    update = {
        "product_id": "201",
        "product_name": "Invalid Update",
        "quantity": "not_a_number",
        "price": "not_a_price",
        "type": "food",
    }
    resp = client.put("/api/products/201", json=update)
    # Should return 400
    assert resp.status_code == 400


def test_delete_product_empty_csv(client, tmp_path: Path):
    # Simulate empty CSV
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("product_id,product_name,quantity,price,type,expiry_date,warranty_period,author,pages\n")
    app = client.application
    app.config["DATA_CSV"] = str(csv_file)
    resp = client.delete("/api/products/1")
    assert resp.status_code == 404

def test_post_product_missing_field(client):
    """Covers 720-721: Missing required field in POST."""
    payload = {"product_name": "Incomplete"}  # Missing other required keys
    resp = client.post("/api/products", json=payload)
    assert resp.status_code == 400
    assert resp.get_json()["error"].lower() == "invalid product data"

def test_post_product_invalid_type(client):
    """Covers 744: Invalid type (e.g., price is a string)."""
    payload = {
        "product_id": 999,
        "product_name": "InvalidPrice",
        "quantity": 5,
        "price": "abc",  # invalid
        "type": "food"
    }
    resp = client.post("/api/products", json=payload)
    assert resp.status_code == 400
    assert resp.get_json()["error"].lower() == "invalid product data"

def test_put_nonexistent_product(client):
    """Covers 868: Trying to update a product that doesn't exist."""
    payload = {
        "product_id": 99999,
        "product_name": "Ghost Product",
        "quantity": 5,
        "price": 9.99,
        "type": "food"
    }
    resp = client.put("/api/products/99999", json=payload)
    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"].lower()

def test_get_product_invalid_id(client):
    """Covers 961: GET with invalid ID format (treated as not found)."""
    resp = client.get("/api/products/invalid-id")
    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"].lower()
