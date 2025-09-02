"""JWT generation, verification, and refresh token utilities."""

from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, Any, Dict, Optional

import jwt
from flask import current_app, request, jsonify, g
from pydantic import BaseModel
from ..models import User

# Default configuration values (used if app config does not provide them)
_DEFAULT_ALGORITHM = "HS256"
_DEFAULT_EXPIRES_MINUTES = 60
_DEFAULT_REFRESH_EXPIRES_DAYS = 30


class TokenPayload(BaseModel):
    """Pydantic model for decoded JWT payload."""
    sub: str
    role: str
    iat: datetime
    exp: datetime


def _get_secret() -> str:
    return current_app.config.get("JWT_SECRET_KEY", "fallback_secret_for_dev")


def _get_algorithm() -> str:
    return current_app.config.get("JWT_ALGORITHM", _DEFAULT_ALGORITHM)


def _get_exp_minutes() -> int:
    return int(current_app.config.get("JWT_EXP_MINUTES", _DEFAULT_EXPIRES_MINUTES))


def create_access_token(user_id: int, role: str, expires_in_minutes: Optional[int] = None) -> str:
    """Create a JWT access token for a user ID with role included."""
    if expires_in_minutes is None:
        expires_in_minutes = _get_exp_minutes()

    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,  # <-- include role
        "iat": now,
        "exp": now + timedelta(minutes=expires_in_minutes),
    }
    secret = _get_secret()
    alg = _get_algorithm()
    token = jwt.encode(payload, secret, algorithm=alg)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def create_refresh_token(user_id: int, role: str, expires_in_days: int = _DEFAULT_REFRESH_EXPIRES_DAYS) -> str:
    """Create a long-lived refresh token with role included."""
    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,  # <-- include role here too
        "iat": now,
        "exp": now + timedelta(days=expires_in_days),
        "type": "refresh"
    }
    secret = _get_secret()
    alg = _get_algorithm()
    token = jwt.encode(payload, secret, algorithm=alg)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token



def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT, returning the payload."""
    secret = _get_secret()
    alg = _get_algorithm()
    return jwt.decode(token, secret, algorithms=[alg])


def jwt_required(func: Optional[Callable] = None) -> Callable:
    """Decorator to protect routes with JWT authentication and set g.current_user_id and g.current_user_role."""

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            token = auth_header.split(" ", 1)[1].strip()
            if not token:
                return jsonify({"error": "Missing token"}), 401

            try:
                payload = decode_access_token(token)
                user_id = payload.get("sub")
                role = payload.get("role")
                if not user_id or not role:
                    return jsonify({"error": "Invalid token payload"}), 401
                g.current_user_id = int(user_id)
                g.current_user_role = role
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return fn(*args, **kwargs)

        return wrapper

    if func:
        return decorator(func)
    return decorator


def roles_required(*allowed_roles: str) -> Callable:
    """Decorator to ensure the authenticated user has one of the allowed roles."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # First ensure user is authenticated
            auth_resp = jwt_required(lambda: None)()
            if auth_resp is not None:
                return auth_resp

            # Check role from g.current_user_role (set in jwt_required)
            if g.current_user_role not in allowed_roles:
                return jsonify({"error": "Forbidden: Insufficient role"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
