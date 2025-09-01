"""Tests for Flask API routes (patched to use JWT and RBAC)."""

def test_get_products_empty(client) -> None:
    """GET /api/products returns empty list when DB is empty (unprotected route)."""
    resp = client.get("/api/products")
    assert resp.status_code == 200
    assert resp.json == []


def test_create_and_get_product(client, make_auth_headers) -> None:
    """POST then GET a product successfully (manager/admin only)."""
    headers = make_auth_headers(role="manager", username="mgr_create", password="pw")
    payload = {
        "product_id": 1,
        "product_name": "Book",
        "quantity": 5,
        "price": 12.5,
        "type": "book",
        "author": "A",
        "pages": 100,
    }
    resp_post = client.post("/api/products", json=payload, headers=headers)
    assert resp_post.status_code == 201, resp_post.json

    resp_get = client.get("/api/products/1")
    assert resp_get.status_code == 200
    assert resp_get.json["product_name"] == "Book"


def test_create_product_invalid_json(client, make_auth_headers) -> None:
    """POST with invalid JSON returns 400 (after passing auth)."""
    headers = make_auth_headers(role="manager", username="mgr_badjson", password="pw")
    resp = client.post("/api/products", data="notjson", headers=headers, content_type="application/json")
    assert resp.status_code == 400


def test_create_product_duplicate(client, make_auth_headers) -> None:
    """POST duplicate product_id returns 409."""
    headers = make_auth_headers(role="manager", username="mgr_dup", password="pw")
    payload = {"product_id": 2, "product_name": "Item", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload, headers=headers)
    resp = client.post("/api/products", json=payload, headers=headers)
    assert resp.status_code == 409


def test_update_product(client, make_auth_headers) -> None:
    """PUT updates an existing product (manager/admin only)."""
    headers = make_auth_headers(role="manager", username="mgr_upd", password="pw")
    payload = {"product_id": 3, "product_name": "Old", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload, headers=headers)
    resp = client.put("/api/products/3", json={"product_name": "New"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json["product_name"] == "New"


def test_update_product_not_found(client, make_auth_headers) -> None:
    """PUT for non-existent product returns 404."""
    headers = make_auth_headers(role="admin", username="admin_upd_nf", password="pw")
    resp = client.put("/api/products/999", json={"product_name": "X"}, headers=headers)
    assert resp.status_code == 404


def test_delete_product(client, make_auth_headers) -> None:
    """DELETE removes existing product (admin only)."""
    admin_headers = make_auth_headers(role="admin", username="admin_del", password="pw")
    payload = {"product_id": 4, "product_name": "ToDel", "quantity": 1, "price": 1.0}
    # Admin can create, too
    client.post("/api/products", json=payload, headers=admin_headers)
    resp = client.delete("/api/products/4", headers=admin_headers)
    # The implementation returns 200 + message (not 204)
    assert resp.status_code == 200
    assert "deleted successfully" in resp.json.get("message", "").lower()


def test_delete_product_not_found(client, make_auth_headers) -> None:
    """DELETE on missing product returns 404 (admin only)."""
    admin_headers = make_auth_headers(role="admin", username="admin_del_nf", password="pw")
    resp = client.delete("/api/products/999", headers=admin_headers)
    assert resp.status_code == 404


def test_post_product_invalid_json_structure(client, make_auth_headers):
    """POST with bad JSON object should return 400."""
    headers = make_auth_headers(role="manager", username="mgr_bad", password="pw")
    resp = client.post("/api/products", json={"nonsense": 123}, headers=headers)
    assert resp.status_code == 400


def test_update_product_invalid_json(client, make_auth_headers):
    """PUT with non-JSON body should return 400."""
    headers = make_auth_headers(role="manager", username="mgr_putbad", password="pw")
    payload = {"product_id": 20, "product_name": "X", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload, headers=headers)
    resp = client.put("/api/products/20", data="notjson", headers=headers, content_type="application/json")
    assert resp.status_code == 400


def test_delete_requires_admin_role(client, make_auth_headers):
    """Managers cannot DELETE products (403)."""
    headers = make_auth_headers(role="manager", username="mgr_del_forbid", password="pw")
    payload = {"product_id": 21, "product_name": "DelX", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload, headers=headers)
    resp = client.delete("/api/products/21", headers=headers)
    assert resp.status_code == 403


def test_get_product_not_found(client):
    """GET for missing product returns 404."""
    resp = client.get("/api/products/99999")
    assert resp.status_code == 404
