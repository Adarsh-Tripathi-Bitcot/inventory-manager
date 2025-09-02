"""Application factory for the Inventory API."""

from __future__ import annotations
from typing import Optional, Dict, Any, Type
import os

from flask import Flask
from dotenv import load_dotenv

from .db import db, migrate
from .routes import api_bp, auth_bp
from .config import get_config
from .seed import seed_db

# Load environment variables from .env
load_dotenv()

# Enable debug logging for JWT issues
# logging.basicConfig(level=logging.DEBUG)


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure a Flask application instance.

    Loads environment variables, sets default config, initializes extensions,
    registers blueprints, and adds CLI commands.

    Args:
        config (Optional[Dict[str, Any]]): Optional dictionary to override default
            Flask configuration. If `None`, environment variables or defaults are used.

    Returns:
        Flask: Configured Flask application instance.
    """
    app: Flask = Flask(__name__)

    # sensible defaults
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # load DB URL from env
    env_db: Optional[str] = os.getenv("DATABASE_URL")
    if env_db:
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", env_db)

    # load JWT config from env
    app.config.setdefault("JWT_SECRET_KEY", os.getenv("JWT_SECRET_KEY", "fallback_secret"))
    app.config.setdefault("JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))
    app.config.setdefault(
        "JWT_EXP_MINUTES", int(os.getenv("JWT_EXP_DELTA_SECONDS", "3600")) // 60
    )

    # allow config override (tests or custom)
    if config:
        app.config.update(config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register pgvector adapter for psycopg2 / psycopg to make SQLAlchemy
    # recommended if you installed `pgvector`.
    try:
        # psycopg2 registration helper
        from pgvector.psycopg2 import register_vector as _register_vector
        from sqlalchemy import event

        @event.listens_for(db.engine, "connect")
        def _on_connect(dbapi_connection, connection_record):
            # arrays=True allows vector arrays usage if needed
            _register_vector(dbapi_connection, arrays=True)
    except Exception:
        # ignore if pgvector not installed or adapter can't be registered
        pass

    # import models after DB init so Flask-Migrate detects them
    with app.app_context():
        from . import models  # noqa: F401

    # register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    # CLI command seed-db
    app.cli.add_command(seed_db)

    return app
