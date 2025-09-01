"""Pytest fixtures for Week 6–7 Inventory API tests (patched for JWT/RBAC)."""

import pytest
from flask import Flask
from week_6_and_7.api.app import create_app
from week_6_and_7.api.db import db as _db


@pytest.fixture
def sample_product() -> dict:
    """Return a sample product dict for testing."""
    return {
        "product_id": 100,
        "product_name": "Sample Product",
        "quantity": 10,
        "price": 25.5,
        "type": "book",
        "author": "Author A",
        "pages": 123,
    }


@pytest.fixture()
def app() -> Flask:
    """Create Flask app with in-memory SQLite database for testing."""
    app: Flask = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture()
def client(app: Flask):
    """Return a Flask test client for making requests."""
    return app.test_client()


@pytest.fixture()
def db(app: Flask):
    """Provide database session for tests."""
    return _db


@pytest.fixture(autouse=True)
def clear_db(db):
    """Clear Product and User tables before each test."""
    from week_6_and_7.api.models import Product, User
    db.session.query(Product).delete()
    db.session.query(User).delete()
    db.session.commit()


# -----------------------
# Auth helper fixtures
# -----------------------

@pytest.fixture
def make_auth_headers(client):
    """
    Helper to create a user (by role) and return Authorization headers with a fresh access token.
    Usage:
        headers = make_auth_headers(role="manager", username="u1", password="pw")
    """
    def _make(role: str = "manager", username: str = "user_mgr", password: str = "pw"):
        # Register (idempotent)
        client.post("/auth/register", json={"username": username, "password": password, "role": role})
        # Login to get token
        resp = client.post("/auth/login", json={"username": username, "password": password})
        assert resp.status_code == 200, f"Login failed for role={role}: {resp.json}"
        token = resp.json["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _make
