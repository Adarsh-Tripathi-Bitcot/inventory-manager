"""API package entrypoint.

This module exposes the Flask application factory function `create_app`
for use in other parts of the project.
"""

from .app import create_app

__all__: list[str] = ["create_app"]
