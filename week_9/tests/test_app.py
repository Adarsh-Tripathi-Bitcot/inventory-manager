"""Tests for Flask app creation."""

from flask import Flask
from week_6_and_7.api.app import create_app


def test_create_app_uses_env(monkeypatch) -> None:
    """App should read DATABASE_URL from environment variable."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///env.db")
    app: Flask = create_app()
    assert "SQLALCHEMY_DATABASE_URI" in app.config
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///env.db"


def test_create_app_with_custom_config() -> None:
    """Custom config passed to create_app overrides defaults."""
    app: Flask = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", "CUSTOM": "X"})
    assert app.config["CUSTOM"] == "X"
