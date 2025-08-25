"""Pytest fixtures for Week 6 Inventory API tests."""

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
        "pages": 123
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
    """Clear Product table before each test."""
    from week_6_and_7.api.models import Product
    db.session.query(Product).delete()
    db.session.commit()