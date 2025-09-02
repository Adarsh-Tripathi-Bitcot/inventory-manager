"""Authentication routes: register, login, and token refresh."""

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from api.db import db
from api.models import User
from api.utils.security import create_access_token, create_refresh_token, decode_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Expected JSON body:
        {
            "username": "<str>",
            "password": "<str>",
            "role": "<str>"  # optional, defaults to 'staff'
        }
    """
    data = request.get_json(force=True, silent=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    username = data["username"].strip()
    password = data["password"]
    role = data.get("role", "staff")  # get role from JSON or default to staff

    if role not in ["admin", "manager", "staff"]:  # validate role
        return jsonify({"error": "Invalid role"}), 400

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username, role=role)  # set role here
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"User {user.username} created successfully", "role": user.role}), 201


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

    access_token = create_access_token(user_id=user.id, role=user.role)
    refresh_token = create_refresh_token(user_id=user.id, role=user.role)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh access + refresh tokens using a valid refresh token.

    Expected JSON body:
        {
            "refresh_token": "<str>"
        }

    Returns:
        JSON response containing new access and refresh tokens.
    """
    data = request.get_json(force=True, silent=True)
    if not data or "refresh_token" not in data:
        return jsonify({"error": "Refresh token required"}), 400

    refresh_token = data["refresh_token"].strip()
    try:
        payload = decode_access_token(refresh_token)

        # Ensure it's a refresh token
        if payload.get("type") != "refresh":
            return jsonify({"error": "Invalid token type"}), 401

        user_id = payload.get("sub")
        role = payload.get("role", "staff")

        if user_id is None:
            return jsonify({"error": "Invalid token payload"}), 401

        # Generate new access + refresh tokens
        new_access_token = create_access_token(user_id=int(user_id), role=role)
        new_refresh_token = create_refresh_token(user_id=int(user_id), role=role)

        return jsonify({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "role": role
        }), 200

    except Exception as e:
        return jsonify({"error": "Invalid or expired refresh token"}), 401
