"""Application factory for the Inventory API."""

from __future__ import annotations
from typing import Optional, Dict, Any
import os

from flask import Flask
from .db import db, migrate
from .routes import api_bp, auth_bp  # ✅ Import both blueprints
from .config import get_config
from .seed import seed_db
from . import models


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config (Optional[Dict[str, Any]]): Optional dictionary to override default
            Flask configuration. If `None`, environment variables or defaults are used.

    Returns:
        Flask: The configured Flask application instance.
    """
    app: Flask = Flask(__name__)

    # Load default configuration
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Load database URL from env if not already provided
    env_db: Optional[str] = os.getenv("DATABASE_URL")
    if env_db:
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", env_db)

    # Load JWT secret key from environment (required for auth)
    jwt_secret: Optional[str] = os.getenv("JWT_SECRET_KEY")
    if jwt_secret:
        app.config["JWT_SECRET_KEY"] = jwt_secret  # used by Flask-JWT-Extended

    # Allow config override (for testing or custom setups)
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure models are imported so Flask-Migrate detects them
    from . import models  # noqa: F401

    # Register blueprints
    app.register_blueprint(api_bp)                 # Existing API routes
    app.register_blueprint(auth_bp, url_prefix="/auth")  # ✅ Auth routes under /auth

    # CLI command for seeding the database
    app.cli.add_command(seed_db)

    return app
