from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Any, List, Optional, Type, Tuple

from flask import Blueprint, current_app, jsonify, request, Response
from pydantic import ValidationError

try:
    from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
except Exception:
    from week_3.inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct

api_bp: Blueprint = Blueprint("api", __name__, url_prefix="/api")

CSV_FIELDS: List[str] = [
    "product_id",
    "product_name",
    "quantity",
    "price",
    "type",
    "expiry_date",
    "warranty_period",
    "author",
    "pages",
]


def _csv_path_from_app() -> Path:
    return Path(current_app.config["DATA_CSV"])


def _read_all_rows(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _write_all_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _build_model_kwargs_for_type(row: Dict[str, Any], model_cls: Type[Product]) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "product_id": row.get("product_id", ""),
        "product_name": row.get("product_name", ""),
        "quantity": row.get("quantity", ""),
        "price": row.get("price", ""),
    }

    if model_cls is FoodProduct:
        base["expiry_date"] = row.get("expiry_date") or None

    elif model_cls is ElectronicProduct:
        wp: Any = row.get("warranty_period")
        base["warranty_period"] = None
        if wp not in (None, ""):
            try:
                base["warranty_period"] = int(wp)
            except (ValueError, TypeError):
                base["warranty_period"] = None

    elif model_cls is BookProduct:
        base["author"] = row.get("author") or None
        pg: Any = row.get("pages")
        base["pages"] = None
        if pg not in (None, ""):
            try:
                base["pages"] = int(pg)
            except (ValueError, TypeError):
                base["pages"] = None

    return base


def _determine_model_class(type_value: str) -> Type[Product]:
    t: str = (type_value or "").strip().lower()
    return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
    type_value: str = row.get("type") or row.get("category") or ""
    model_cls: Type[Product] = _determine_model_class(type_value)
    kwargs: Dict[str, Any] = _build_model_kwargs_for_type(row, model_cls)
    try:
        return model_cls(**kwargs)
    except ValidationError:
        return None


def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
    dumped: Dict[str, Any] = model.model_dump()
    return {
        "product_id": str(dumped.get("product_id") or ""),
        "product_name": str(dumped.get("product_name") or ""),
        "quantity": str(dumped.get("quantity") or ""),
        "price": str(dumped.get("price") or ""),
        "type": type_value,
        "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
        "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
        "author": str(dumped.get("author") or ""),
        "pages": str(dumped.get("pages") or "") if dumped.get("pages") is not None else "",
    }


@api_bp.route("/products", methods=["GET"])
def get_products() -> Tuple[Response, int]:
    csv_path: Path = _csv_path_from_app()
    rows: List[Dict[str, str]] = _read_all_rows(csv_path)
    products: List[Dict[str, Any]] = [m.model_dump() for r in rows if (m := _row_to_model(r))]
    return jsonify(products), 200


@api_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id: str) -> Tuple[Response, int]:
    csv_path: Path = _csv_path_from_app()
    for r in _read_all_rows(csv_path):
        if (r.get("product_id") or "") == product_id:
            if (m := _row_to_model(r)):
                return jsonify(m.model_dump()), 200
            break
    return jsonify({"error": "Product not found"}), 404


@api_bp.route("/products", methods=["POST"])
def create_product() -> Tuple[Response, int]:
    body: Optional[Dict[str, Any]] = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    requested_type: str = (body.get("type") or "").strip().lower()
    model_cls: Type[Product] = _determine_model_class(requested_type)
    ctor_kwargs: Dict[str, Any] = _build_model_kwargs_for_type(body, model_cls)

    try:
        product: Product = model_cls(**ctor_kwargs)
        final_type: str = requested_type
    except ValidationError:
        if model_cls in (ElectronicProduct, BookProduct):
            fallback_fields: Dict[str, Any] = {
                "product_id": ctor_kwargs.get("product_id", ""),
                "product_name": ctor_kwargs.get("product_name", ""),
                "quantity": ctor_kwargs.get("quantity", ""),
                "price": ctor_kwargs.get("price", ""),
            }
            try:
                product = Product(**fallback_fields)
                final_type = ""
            except ValidationError as ve:
                return jsonify({"error": str(ve)}), 400
        else:
            return jsonify({"error": "Invalid product data"}), 400

    csv_path: Path = _csv_path_from_app()
    rows: List[Dict[str, str]] = _read_all_rows(csv_path)

    if any((r.get("product_id") or "") == product.product_id for r in rows):
        return jsonify({"error": "Product with this product_id already exists"}), 409

    rows.append(_model_to_csv_row(product, final_type))
    _write_all_rows(csv_path, rows)

    result: Dict[str, Any] = product.model_dump()
    if requested_type == "book":
        result.setdefault("pages", None)
        result.setdefault("author", None)
    elif requested_type == "electronic":
        result.setdefault("warranty_period", None)
    elif requested_type == "food":
        result.setdefault("expiry_date", None)

    return jsonify(result), 201


@api_bp.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id: str) -> Tuple[Response, int]:
    body: Optional[Dict[str, Any]] = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    csv_path: Path = _csv_path_from_app()
    rows: List[Dict[str, str]] = _read_all_rows(csv_path)

    existing_row_index: Optional[int] = None
    for idx, r in enumerate(rows):
        if (r.get("product_id") or "") == product_id:
            existing_row_index = idx
            break
    if existing_row_index is None:
        return jsonify({"error": "Product not found"}), 404

    type_value: str = (body.get("type") or "").strip().lower()
    model_cls: Type[Product] = _determine_model_class(type_value)
    ctor_kwargs: Dict[str, Any] = _build_model_kwargs_for_type(body, model_cls)

    try:
        product: Product = model_cls(**ctor_kwargs)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    rows[existing_row_index] = _model_to_csv_row(product, type_value)
    _write_all_rows(csv_path, rows)
    return jsonify(product.model_dump()), 200


@api_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id: str) -> Tuple[Response, int] | Tuple[str, int]:
    csv_path: Path = _csv_path_from_app()
    rows: List[Dict[str, str]] = _read_all_rows(csv_path)
    new_rows: List[Dict[str, str]] = [r for r in rows if (r.get("product_id") or "") != product_id]

    if len(new_rows) == len(rows):
        return jsonify({"error": "Product not found"}), 404

    _write_all_rows(csv_path, new_rows)
    return "", 204
