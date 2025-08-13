# api/routes/products.py
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Optional, Type

from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

# Try importing models from possible package locations (flexible for your repo layout)
try:
    from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
except Exception:
    from week_3.inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct

api_bp = Blueprint("api", __name__, url_prefix="/api")

CSV_FIELDS = [
    "product_id",
    "product_name",
    "quantity",
    "price",
    "type",  # maps to product category (food, electronic, book)
    "expiry_date",
    "warranty_period",
    "author",
    "pages",
]


def _csv_path_from_app() -> Path:
    """Return Path object of the configured CSV for this app instance."""
    return Path(current_app.config["DATA_CSV"])


def _read_all_rows(csv_path: Path) -> List[Dict[str, str]]:
    """Read CSV rows (returns [] if file not present)."""
    if not csv_path.exists():
        return []
    with csv_path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]


def _write_all_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    """Write all CSV rows (overwrites). Ensures header is present."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _build_model_kwargs_for_type(row: Dict[str, str], model_cls: Type[Product]) -> Dict[str, Any]:
    """
    Convert a CSV row into kwargs appropriate for the target model class.

    Only includes fields that the model expects to avoid unknown-field errors.
    """
    base = {
        "product_id": row.get("product_id", ""),
        "product_name": row.get("product_name", ""),
        "quantity": row.get("quantity", ""),
        "price": row.get("price", ""),
    }
    if model_cls is FoodProduct:
        base["expiry_date"] = row.get("expiry_date") or None
    elif model_cls is ElectronicProduct:
        wp = row.get("warranty_period")
        base["warranty_period"] = int(wp) if wp and wp.strip() else None
    elif model_cls is BookProduct:
        base["author"] = row.get("author") or None
        pg = row.get("pages")
        base["pages"] = int(pg) if pg and pg.strip() else None
    return base


def _determine_model_class(type_value: str) -> Type[Product]:
    """Return the appropriate Pydantic class for a given type string."""
    t = (type_value or "").strip().lower()
    return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
    """
    Convert a CSV row into a validated Pydantic model.
    Returns None when validation fails (invalid row).
    """
    # support both 'type' and legacy 'category' column names
    type_value = row.get("type") or row.get("category") or ""
    model_cls = _determine_model_class(type_value)
    kwargs = _build_model_kwargs_for_type(row, model_cls)
    try:
        return model_cls(**kwargs)
    except ValidationError:
        # skip invalid rows when reading the CSV for GET endpoints
        return None


def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
    """
    Convert a Pydantic model to a CSV row using our canonical CSV_FIELDS.
    Ensures every CSV column is present as a string.
    """
    dumped = model.model_dump()
    return {
        "product_id": str(dumped.get("product_id", "") or ""),
        "product_name": str(dumped.get("product_name", "") or ""),
        "quantity": str(dumped.get("quantity", "") or ""),
        "price": str(dumped.get("price", "") or ""),
        "type": type_value,
        "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
        "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
        "author": str(dumped.get("author") or ""),
        "pages": str(dumped.get("pages") or "") if dumped.get("pages") is not None else "",
    }


@api_bp.route("/products", methods=["GET"])
def get_products():
    """
    GET /api/products
    Returns:
        JSON list of products (only validated rows).
    """
    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)
    products = []
    for r in rows:
        model = _row_to_model(r)
        if model:
            products.append(model.model_dump())
    return jsonify(products), 200


@api_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id: str):
    """
    GET /api/products/<product_id>
    Returns:
        Product JSON or 404.
    """
    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)
    for r in rows:
        if (r.get("product_id") or "") == product_id:
            model = _row_to_model(r)
            if model:
                return jsonify(model.model_dump()), 200
            # found row but invalid -> treat as not found for API simplicity
            break
    return jsonify({"error": "Product not found"}), 404



@api_bp.route("/products", methods=["POST"])
def create_product():
    """
    POST /api/products
    Body must be JSON representing the product and must include a 'type' field
    (one of "food", "electronic", "book", or omitted for generic product).
    Validates using Pydantic model and appends a row to configured CSV.

    Responses:
        201: created, returns created product
        400: validation error / bad request
        409: conflict (product_id already exists)
    """
    body = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    type_value = (body.get("type") or "").strip().lower()
    model_cls = _determine_model_class(type_value)

    # prepare constructor kwargs per model class
    ctor_kwargs = {}
    try:
        # reuse the same keys the _build_model_kwargs_for_type expects
        ctor_kwargs = _build_model_kwargs_for_type(
            {
                "product_id": body.get("product_id", ""),
                "product_name": body.get("product_name", ""),
                "quantity": body.get("quantity", ""),
                "price": body.get("price", ""),
                "expiry_date": body.get("expiry_date", ""),
                "warranty_period": body.get("warranty_period", ""),
                "author": body.get("author", ""),
                "pages": body.get("pages", ""),
            },
            model_cls,
        )
        product = model_cls(**ctor_kwargs)
    except ValidationError as e:
        return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)

    # conflict check
    if any((r.get("product_id") or "") == product.product_id for r in rows):
        return jsonify({"error": "Product with this product_id already exists"}), 409

    # append
    row = _model_to_csv_row(product, type_value)
    rows.append(row)
    _write_all_rows(csv_path, rows)
    return jsonify(product.model_dump()), 201


@api_bp.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id: str):
    """
    PUT /api/products/<product_id>
    Replaces the product with the provided JSON payload (validated with Pydantic).
    Returns:
        200 + updated product JSON on success
        400 on validation error
        404 if product not present
    """
    body = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    type_value = (body.get("type") or "").strip().lower()
    model_cls = _determine_model_class(type_value)

    # build constructor kwargs and validate
    try:
        ctor_kwargs = _build_model_kwargs_for_type(
            {
                "product_id": body.get("product_id", product_id),
                "product_name": body.get("product_name", ""),
                "quantity": body.get("quantity", ""),
                "price": body.get("price", ""),
                "expiry_date": body.get("expiry_date", ""),
                "warranty_period": body.get("warranty_period", ""),
                "author": body.get("author", ""),
                "pages": body.get("pages", ""),
            },
            model_cls,
        )
        product = model_cls(**ctor_kwargs)
    except ValidationError as e:
        return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)

    found = False
    for idx, r in enumerate(rows):
        if (r.get("product_id") or "") == product_id:
            # replace row
            rows[idx] = _model_to_csv_row(product, type_value)
            found = True
            break

    if not found:
        return jsonify({"error": "Product not found"}), 404

    _write_all_rows(csv_path, rows)
    return jsonify(product.model_dump()), 200


@api_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id: str):
    """
    DELETE /api/products/<product_id>
    Removes the product with the given ID from the CSV.

    Returns:
        204 No Content on successful delete
        404 Not Found if the product does not exist
    """
    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)

    # Filter out the product to delete
    new_rows = [r for r in rows if (r.get("product_id") or "") != product_id]

    if len(new_rows) == len(rows):
        return jsonify({"error": "Product not found"}), 404

    _write_all_rows(csv_path, new_rows)
    # No body for 204 per HTTP spec
    return "", 204
