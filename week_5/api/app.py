# # api/app.py
# from pathlib import Path
# from typing import Optional, Dict, Any
# from flask import Flask

# from .routes.products import api_bp

# def _default_data_csv_path() -> str:
#     """
#     Compute default path to the products CSV.
#     Assumes project root layout: <repo-root>/week_3/inventory_manager/data/products.csv
#     """
#     return str(Path.cwd() / "week_3" / "data" / "products.csv")

# def create_app(config_overrides: Optional[Dict[str, Any]] = None) -> Flask:
#     """
#     Create and configure the Flask application.

#     Args:
#         config_overrides: Optional dict to override app config values (useful for tests).

#     Returns:
#         Configured Flask application.
#     """
#     app = Flask(__name__)
#     # default config (can be overridden when calling create_app)
#     app.config.setdefault("DATA_CSV", _default_data_csv_path())

#     if config_overrides:
#         app.config.update(config_overrides)

#     app.register_blueprint(api_bp)
#     return app

# if __name__ == "__main__":
#     # quick dev run
#     create_app().run(debug=True)


# week_5/api/app.py
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



