# """JWT generation and verification utilities."""

# from datetime import datetime, timedelta
# from functools import wraps
# from typing import Callable, Any, Dict, Optional

# import jwt
# from flask import current_app, request, jsonify, g
# import logging

# # Default configuration values (used if app config does not provide them)
# _DEFAULT_ALGORITHM = "HS256"
# _DEFAULT_EXPIRES_MINUTES = 60


# def _get_secret() -> str:
#     """Return JWT secret key from Flask config (or fallback)."""
#     return current_app.config.get("JWT_SECRET_KEY", "fallback_secret_for_dev")


# def _get_algorithm() -> str:
#     return current_app.config.get("JWT_ALGORITHM", _DEFAULT_ALGORITHM)


# def _get_exp_minutes() -> int:
#     return int(current_app.config.get("JWT_EXP_MINUTES", _DEFAULT_EXPIRES_MINUTES))

# def create_access_token(user_id: int, expires_in_minutes: Optional[int] = None) -> str:
#     if expires_in_minutes is None:
#         expires_in_minutes = _get_exp_minutes()

#     now = datetime.utcnow()
#     payload: Dict[str, Any] = {
#         "sub": str(user_id),  # <-- string now
#         "iat": now,
#         "exp": now + timedelta(minutes=expires_in_minutes),
#     }
#     secret = _get_secret()
#     alg = _get_algorithm()
#     logging.debug(f"Creating token for user_id={user_id} with secret={secret} and algorithm={alg}")
#     token = jwt.encode(payload, secret, algorithm=alg)
#     if isinstance(token, bytes):
#         token = token.decode("utf-8")
#     logging.debug(f"Token created: {token}")
#     return token


# def decode_access_token(token: str) -> Dict[str, Any]:
#     """Decode and validate JWT, returning the payload.

#     Raises jwt.* exceptions on errors.
#     """
#     secret = current_app.config.get("JWT_SECRET_KEY", "fallback_secret_for_dev")
#     alg = current_app.config.get("JWT_ALGORITHM", "HS256")
#     logging.debug(f"Decoding token with secret={secret} and algorithm={alg}")
#     # return jwt.decode(token, _get_secret(), algorithms=[_get_algorithm()])
#     return jwt.decode(token, secret, algorithms=[alg])

# def jwt_required(func: Callable) -> Callable:
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         auth_header = request.headers.get("Authorization", "")
#         logging.debug(f"Authorization header received: {auth_header}")

#         if not auth_header.startswith("Bearer "):
#             logging.debug("Authorization header missing or invalid format")
#             return jsonify({"error": "Missing or invalid Authorization header"}), 401

#         token = auth_header.split(" ", 1)[1].strip()
#         logging.debug(f"Extracted token: {token}")

#         if not token:
#             logging.debug("Token is empty after parsing")
#             return jsonify({"error": "Missing token"}), 401

#         try:
#             payload = decode_access_token(token)
#             logging.debug(f"Token payload decoded successfully: {payload}")
#             user_id = payload.get("sub")
#             if user_id is None:
#                 logging.debug("Token payload does not contain user_id")
#                 return jsonify({"error": "Invalid token payload"}), 401
#             g.current_user_id = int(user_id)
#         except jwt.ExpiredSignatureError:
#             logging.debug("Token has expired")
#             return jsonify({"error": "Token has expired"}), 401
#         except jwt.InvalidTokenError as e:
#             logging.debug(f"Invalid token error: {e}")
#             return jsonify({"error": "Invalid token"}), 401

#         return func(*args, **kwargs)

#     return wrapper






"""JWT generation, verification, and refresh token utilities."""

from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Any, Dict, Optional
import logging

import jwt
from flask import current_app, request, jsonify, g
from pydantic import BaseModel

# Default configuration values (used if app config does not provide them)
_DEFAULT_ALGORITHM = "HS256"
_DEFAULT_EXPIRES_MINUTES = 60
_DEFAULT_REFRESH_EXPIRES_DAYS = 30


class TokenPayload(BaseModel):
    """Pydantic model for decoded JWT payload."""

    sub: str
    iat: datetime
    exp: datetime


def _get_secret() -> str:
    """Return JWT secret key from Flask config (or fallback)."""
    return current_app.config.get("JWT_SECRET_KEY", "fallback_secret_for_dev")


def _get_algorithm() -> str:
    """Return JWT algorithm from Flask config (or default)."""
    return current_app.config.get("JWT_ALGORITHM", _DEFAULT_ALGORITHM)


def _get_exp_minutes() -> int:
    """Return access token expiration in minutes from config."""
    return int(current_app.config.get("JWT_EXP_MINUTES", _DEFAULT_EXPIRES_MINUTES))


def create_access_token(user_id: int, expires_in_minutes: Optional[int] = None) -> str:
    """Create a JWT access token for a user ID.

    Args:
        user_id (int): ID of the user.
        expires_in_minutes (Optional[int]): Expiration time in minutes. Defaults to config.

    Returns:
        str: Encoded JWT token.
    """
    if expires_in_minutes is None:
        expires_in_minutes = _get_exp_minutes()

    now = datetime.utcnow()
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=expires_in_minutes),
    }
    secret = _get_secret()
    alg = _get_algorithm()
    logging.debug(f"Creating token for user_id={user_id} with secret={secret} and algorithm={alg}")
    token = jwt.encode(payload, secret, algorithm=alg)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    logging.debug(f"Token created: {token}")
    return token


def create_refresh_token(user_id: int, expires_in_days: int = _DEFAULT_REFRESH_EXPIRES_DAYS) -> str:
    """Create a long-lived refresh token.

    Args:
        user_id (int): ID of the user.
        expires_in_days (int): Expiration in days. Defaults to 30.

    Returns:
        str: Encoded refresh JWT token.
    """
    now = datetime.utcnow()
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(days=expires_in_days),
        "type": "refresh"
    }
    secret = _get_secret()
    alg = _get_algorithm()
    logging.debug(f"Creating refresh token for user_id={user_id}")
    token = jwt.encode(payload, secret, algorithm=alg)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    logging.debug(f"Refresh token created: {token}")
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT, returning the payload.

    Args:
        token (str): JWT token string.

    Returns:
        Dict[str, Any]: Decoded payload.

    Raises:
        jwt.ExpiredSignatureError: If token is expired.
        jwt.InvalidTokenError: If token is invalid.
    """
    secret = _get_secret()
    alg = _get_algorithm()
    logging.debug(f"Decoding token with secret={secret} and algorithm={alg}")
    return jwt.decode(token, secret, algorithms=[alg])


def jwt_required(func: Callable) -> Callable:
    """Decorator to protect routes with JWT authentication.

    Sets `g.current_user_id` to the integer user ID.

    Args:
        func (Callable): Route handler function.

    Returns:
        Callable: Wrapped function with JWT authentication.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        logging.debug(f"Authorization header received: {auth_header}")

        if not auth_header.startswith("Bearer "):
            logging.debug("Authorization header missing or invalid format")
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        logging.debug(f"Extracted token: {token}")

        if not token:
            logging.debug("Token is empty after parsing")
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = decode_access_token(token)
            logging.debug(f"Token payload decoded successfully: {payload}")
            user_id = payload.get("sub")
            if user_id is None:
                logging.debug("Token payload does not contain user_id")
                return jsonify({"error": "Invalid token payload"}), 401
            g.current_user_id = int(user_id)
        except jwt.ExpiredSignatureError:
            logging.debug("Token has expired")
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            logging.debug(f"Invalid token error: {e}")
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper
