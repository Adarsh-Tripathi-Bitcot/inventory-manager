# """Configuration management for the Inventory API."""

# import os
# from dotenv import load_dotenv
# from typing import Type, Optional

# # Load .env (project root) if present
# load_dotenv()


# class BaseConfig:
#     """Base configuration shared across all environments."""

#     SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
#     # Standardized env var name: JWT_SECRET_KEY
#     JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret_for_dev")


# class DevConfig(BaseConfig):
#     """Development configuration using DATABASE_URL from environment."""

#     SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")


# class TestConfig(BaseConfig):
#     """Testing configuration with fallback local SQLite / Postgres test DB."""

#     SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL") or (
#         "sqlite:///:memory:"
#     )


# config_map: dict[str, Type[BaseConfig]] = {
#     "default": DevConfig,
#     "testing": TestConfig,
# }


# def get_config(name: Optional[str] = None) -> Type[BaseConfig]:
#     """Return a configuration class based on name.

#     Args:
#         name (Optional[str]): Name of config ("default" or "testing").
#             If None or invalid, defaults to DevConfig.

#     Returns:
#         Type[BaseConfig]: Selected configuration class.
#     """
#     if name and name in config_map:
#         return config_map[name]
#     return config_map["default"]




"""Configuration management for the Inventory API."""

import os
from dotenv import load_dotenv
from typing import Type, Optional

# Load .env (project root) if present
load_dotenv()


class BaseConfig:
    """Base configuration shared across all environments.

    Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy modification tracking flag.
        JWT_SECRET_KEY (str): Secret key for JWT encoding/decoding.
    """

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "fallback_secret_for_dev")


class DevConfig(BaseConfig):
    """Development configuration using DATABASE_URL from environment.

    Attributes:
        SQLALCHEMY_DATABASE_URI (Optional[str]): Database URI loaded from env.
    """

    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")


class TestConfig(BaseConfig):
    """Testing configuration with fallback local SQLite / Postgres test DB.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): Database URI for testing.
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL") or (
        "sqlite:///:memory:"
    )


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
