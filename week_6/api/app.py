"""Application factory for the Inventory API."""

from __future__ import annotations
from typing import Optional, Dict, Any
import os

from flask import Flask

from .db import db, migrate
from .routes import api_bp
from .config import get_config


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config (Optional[Dict[str, Any]]): Optional dictionary to override default
            Flask configuration. If `None`, environment variables or defaults are used.

    Returns:
        Flask: The configured Flask application instance.
    """
    app: Flask = Flask(__name__)

    # sensible defaults
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    env_db: Optional[str] = os.getenv("DATABASE_URL")
    if env_db:
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", env_db)

    # Allow callers (tests) to override config by passing a dict
    if config:
        app.config.update(config)

    # init extensions
    db.init_app(app)

    # ensure models are imported so Flask-Migrate sees them
    from . import models  # noqa: F401

    migrate.init_app(app, db)

    app.register_blueprint(api_bp)

    # CLI command seed-db
    from .seed import seed_db
    app.cli.add_command(seed_db)

    return app
