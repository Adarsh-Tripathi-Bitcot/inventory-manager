"""Product-related API routes."""

from typing import Type, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError, BaseModel

from ..db import db
from ..models import Product
from ..schemas import (
    FoodProductCreate,
    ElectronicProductCreate,
    BookProductCreate,
    GenericProductCreate,
    ProductUpdate,
    ProductResponse,
)

api_bp: Blueprint = Blueprint("api", __name__, url_prefix="/api")


def _choose_create_schema(product_type: str) -> Type[BaseModel]:
    """Return correct Pydantic schema based on product type.

    Args:
        product_type (str): Type of the product ("food", "electronic", "book").

    Returns:
        Type[BaseModel]: Corresponding Pydantic request model.
    """
    type_map: dict[str, Type[BaseModel]] = {
        "food": FoodProductCreate,
        "electronic": ElectronicProductCreate,
        "book": BookProductCreate,
    }
    return type_map.get(product_type.lower().strip(), GenericProductCreate)


@api_bp.route("/products", methods=["GET"])
def get_products() -> Tuple[Response, int]:
    """Fetch all products."""
    products: list[Product] = Product.query.all()
    return jsonify([ProductResponse.model_validate(p).model_dump() for p in products]), 200


@api_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Tuple[Response, int]:
    """Fetch a single product by ID."""
    product: Product | None = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(ProductResponse.model_validate(product).model_dump()), 200


@api_bp.route("/products", methods=["POST"])
def create_product() -> Tuple[Response, int]:
    """Create a new product."""
    data: dict[str, Any] | None = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    schema_cls: Type[BaseModel] = _choose_create_schema(data.get("type", ""))

    try:
        product_in: BaseModel = schema_cls(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if Product.query.filter_by(product_id=product_in.product_id).first():
        return jsonify({"error": "Product with this product_id already exists"}), 409

    product: Product = Product(**product_in.model_dump())
    db.session.add(product)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(ProductResponse.model_validate(product).model_dump()), 201


@api_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> Tuple[Response, int]:
    """Update an existing product."""
    data: dict[str, Any] | None = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    product: Product | None = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        update_in: ProductUpdate = ProductUpdate(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    updates: dict[str, Any] = update_in.model_dump(exclude_unset=True)
    for key, val in updates.items():
        setattr(product, key, val)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify(ProductResponse.model_validate(product).model_dump()), 200


@api_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> Tuple[str | Response, int]:
    """Delete a product."""
    product: Product | None = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return "", 204