"""Configuration management for the Inventory API."""

import os
from dotenv import load_dotenv
from typing import Type, Optional

load_dotenv()  # Load .env file in project root


class BaseConfig:
    """Base configuration shared across all environments."""

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class DevConfig(BaseConfig):
    """Development configuration using DATABASE_URL from environment."""

    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret")


class TestConfig(BaseConfig):
    """Testing configuration with fallback local PostgreSQL test DB."""

    SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL") or (
        "postgresql://postgres:postgres@localhost/inventory_test_db"
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret")


config_map: dict[str, Type[BaseConfig]] = {
    "default": DevConfig,
    "testing": TestConfig,
}


def get_config(name: Optional[str] = None) -> Type[BaseConfig]:
    """Return a configuration class based on name.

    Args:
        name (Optional[str]): Name of config ("default" or "testing").
            If None or invalid, defaults to DevConfig.

    Returns:
        Type[BaseConfig]: Selected configuration class.
    """
    if name and name in config_map:
        return config_map[name]
    return config_map["default"]
