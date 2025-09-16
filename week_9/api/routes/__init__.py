"""Blueprint exports for API routes."""

from .products import api_bp
from .auth_routes import auth_bp

__all__: list[str] = ["api_bp", "auth_bp"]
