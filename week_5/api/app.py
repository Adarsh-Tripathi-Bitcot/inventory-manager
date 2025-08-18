from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask
from .routes.products import api_bp


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """
    Flask application factory.

    Args:
        config (Optional[Dict[str, Any]]): Optional dictionary of configuration values.
            Supported keys:
              - "DATA_CSV": str → path to the products CSV file.

    Returns:
        Flask: The configured Flask application instance.
    """
    app: Flask = Flask(__name__)

    # Sensible default CSV path (overridden by tests via create_app({...}))
    default_csv: Path = Path.cwd() / "data" / "products.csv"
    app.config.update(
        DATA_CSV=str(default_csv),
    )

    if config is not None:
        app.config.update(config)

    # Register blueprints
    app.register_blueprint(api_bp)

    return app
