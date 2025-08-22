"""Tests for Flask API routes."""

import pytest

def test_get_products_empty(client) -> None:
    """GET /api/products returns empty list when DB is empty."""
    resp = client.get("/api/products")
    assert resp.status_code == 200
    assert resp.json == []


def test_create_and_get_product(client) -> None:
    """POST then GET a product successfully."""
    payload = {"product_id": 1, "product_name": "Book", "quantity": 5, "price": 12.5, "type": "book", "author": "A", "pages": 100}
    resp_post = client.post("/api/products", json=payload)
    assert resp_post.status_code == 201

    resp_get = client.get("/api/products/1")
    assert resp_get.status_code == 200
    assert resp_get.json["product_name"] == "Book"


def test_create_product_invalid_json(client) -> None:
    """POST with invalid JSON returns 400."""
    resp = client.post("/api/products", data="notjson")
    assert resp.status_code == 400


def test_create_product_duplicate(client) -> None:
    """POST duplicate product_id returns 409."""
    payload = {"product_id": 2, "product_name": "Item", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload)
    resp = client.post("/api/products", json=payload)
    assert resp.status_code == 409


def test_update_product(client) -> None:
    """PUT updates an existing product."""
    payload = {"product_id": 3, "product_name": "Old", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload)
    resp = client.put("/api/products/3", json={"product_name": "New"})
    assert resp.status_code == 200
    assert resp.json["product_name"] == "New"


def test_update_product_not_found(client) -> None:
    """PUT for non-existent product returns 404."""
    resp = client.put("/api/products/999", json={"product_name": "X"})
    assert resp.status_code == 404


def test_delete_product(client) -> None:
    """DELETE removes existing product."""
    payload = {"product_id": 4, "product_name": "ToDel", "quantity": 1, "price": 1.0}
    client.post("/api/products", json=payload)
    resp = client.delete("/api/products/4")
    assert resp.status_code == 204


def test_delete_product_not_found(client) -> None:
    """DELETE on missing product returns 404."""
    resp = client.delete("/api/products/999")
    assert resp.status_code == 404