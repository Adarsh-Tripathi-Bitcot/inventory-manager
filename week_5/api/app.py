from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask

from .routes.products import api_bp


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """
    Flask application factory.

    Config keys you can pass:
      - DATA_CSV: path to the products CSV file.
    """
    app = Flask(__name__)

    # Sensible default CSV path (overridden by tests via create_app({...}))
    default_csv = Path.cwd() / "data" / "products.csv"
    app.config.update(
        DATA_CSV=str(default_csv),
    )

    if config:
        app.config.update(config)

    # Register blueprints
    app.register_blueprint(api_bp)

    return app



