"""Configuration management for the Inventory API.

Provides configuration classes for different environments (development, testing).
Supports loading environment variables from a `.env` file.
"""

import os
from dotenv import load_dotenv
from typing import Type

load_dotenv()  # loads .env in project root if present


class BaseConfig:
    """Base configuration shared across all environments."""

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class DevConfig(BaseConfig):
    """Development configuration using DATABASE_URL from environment."""

    SQLALCHEMY_DATABASE_URI: str | None = os.getenv("DATABASE_URL")


class TestConfig(BaseConfig):
    """Testing configuration with fallback local PostgreSQL test DB."""

    SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL") or (
        "postgresql://postgres:postgres@localhost/inventory_test_db"
    )


config_map: dict[str, Type[BaseConfig]] = {
    "default": DevConfig,
    "testing": TestConfig,
}


def get_config(name: str | None = None) -> Type[BaseConfig]:
    """Return a config class based on name.

    Args:
        name (str | None): Name of the config ("default" or "testing").
            If None or invalid, defaults to DevConfig.

    Returns:
        Type[BaseConfig]: A configuration class.
    """
    if name and name in config_map:
        return config_map[name]
    return config_map["default"]
