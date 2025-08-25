from flask import Blueprint, request, jsonify
from ..models import db, User
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Any, Dict

auth_bp = Blueprint("auth", __name__)

class RegisterRequest(BaseModel):
    """
    Schema for user registration request using Pydantic.

    Attributes:
        username (str): The desired username of the user.
        email (EmailStr): The email address of the user.
        password (str): The password chosen by the user.
    """
    username: str
    email: EmailStr
    password: str

@auth_bp.route("/register", methods=["POST"])
def register() -> tuple[Dict[str, Any], int]:
    """
    Handle user registration.

    Returns:
        tuple: A JSON response and corresponding HTTP status code.

    Raises:
        400 Bad Request: If required fields are missing, user already exists,
                         or if the input format is invalid.
        201 Created: When the user is successfully registered.
    """
    try:
        data = RegisterRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if User.query.filter((User.username == data.username) | (User.email == data.email)).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=data.username, email=data.email)
    user.set_password(data.password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
