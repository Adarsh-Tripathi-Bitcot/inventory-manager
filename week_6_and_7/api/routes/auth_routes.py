# """Authentication routes: register and login."""

# from flask import Blueprint, request, jsonify, current_app
# from sqlalchemy.exc import SQLAlchemyError

# from week_6_and_7.api.db import db
# from week_6_and_7.api.models import User
# from week_6_and_7.api.utils.security import create_access_token
# import logging

# auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# @auth_bp.route("/register", methods=["POST"])
# def register():
#     """Register a new user.

#     Expected JSON body: {"username": "<str>", "password": "<str>"}
#     """
#     data = request.get_json(force=True, silent=True)
#     if not data or "username" not in data or "password" not in data:
#         return jsonify({"error": "Username and password required"}), 400

#     username = data["username"].strip()
#     password = data["password"]

#     if not username or not password:
#         return jsonify({"error": "Username and password required"}), 400

#     if User.query.filter_by(username=username).first():
#         return jsonify({"error": "Username already exists"}), 409

#     user = User(username=username)
#     user.set_password(password)

#     db.session.add(user)
#     try:
#         db.session.commit()
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500

#     return jsonify({"message": f"User {user.username} created successfully"}), 201


# @auth_bp.route("/login", methods=["POST"])
# def login():
#     """Authenticate user and return JWT token.

#     Expected JSON body: {"username": "<str>", "password": "<str>"}
#     """
#     data = request.get_json(force=True, silent=True)
#     if not data or "username" not in data or "password" not in data:
#         return jsonify({"error": "Username and password required"}), 400

#     username = data["username"].strip()
#     password = data["password"]

#     user = User.query.filter_by(username=username).first()
#     if not user or not user.check_password(password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     token = create_access_token(user_id=user.id)
#     logging.debug(f"Login successful. user_id={user.id}, token={token}")
#     return jsonify({"token": token}), 200






"""Authentication routes: register, login, and token refresh."""

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import logging

from week_6_and_7.api.db import db
from week_6_and_7.api.models import User
from week_6_and_7.api.utils.security import create_access_token, create_refresh_token, decode_access_token, jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Expected JSON body:
        {
            "username": "<str>",
            "password": "<str>"
        }

    Returns:
        JSON response with status code.
    """
    data = request.get_json(force=True, silent=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    username = data["username"].strip()
    password = data["password"]

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"User {user.username} created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return access + refresh tokens.

    Expected JSON body:
        {
            "username": "<str>",
            "password": "<str>"
        }

    Returns:
        JSON response containing access and refresh tokens.
    """
    data = request.get_json(force=True, silent=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    username = data["username"].strip()
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(user_id=user.id)
    logging.debug(f"Login successful. user_id={user.id}, access_token={access_token}, refresh_token={refresh_token}")
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh access token using a valid refresh token.

    Expected JSON body:
        {
            "refresh_token": "<str>"
        }

    Returns:
        JSON response containing new access token.
    """
    data = request.get_json(force=True, silent=True)
    if not data or "refresh_token" not in data:
        return jsonify({"error": "Refresh token required"}), 400

    refresh_token = data["refresh_token"].strip()
    try:
        payload = decode_access_token(refresh_token)
        if payload.get("type") != "refresh":
            return jsonify({"error": "Invalid token type"}), 401

        user_id = payload.get("sub")
        if user_id is None:
            return jsonify({"error": "Invalid token payload"}), 401

        new_access_token = create_access_token(user_id=int(user_id))
        return jsonify({"access_token": new_access_token}), 200
    except Exception as e:
        logging.debug(f"Refresh token invalid or expired: {e}")
        return jsonify({"error": "Invalid or expired refresh token"}), 401
