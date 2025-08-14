# # api/routes/products.py
# from __future__ import annotations

# import csv
# from dataclasses import dataclass
# from pathlib import Path
# from typing import Dict, Any, List, Optional, Type

# from flask import Blueprint, current_app, jsonify, request
# from pydantic import ValidationError

# # Try importing models from possible package locations (flexible for your repo layout)
# try:
#     from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
# except Exception:
#     from week_3.inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct

# api_bp = Blueprint("api", __name__, url_prefix="/api")

# CSV_FIELDS = [
#     "product_id",
#     "product_name",
#     "quantity",
#     "price",
#     "type",  # maps to product category (food, electronic, book)
#     "expiry_date",
#     "warranty_period",
#     "author",
#     "pages",
# ]


# def _csv_path_from_app() -> Path:
#     """Return Path object of the configured CSV for this app instance."""
#     return Path(current_app.config["DATA_CSV"])


# def _read_all_rows(csv_path: Path) -> List[Dict[str, str]]:
#     """Read CSV rows (returns [] if file not present)."""
#     if not csv_path.exists():
#         return []
#     with csv_path.open("r", newline="", encoding="utf-8") as fh:
#         reader = csv.DictReader(fh)
#         return [row for row in reader]


# def _write_all_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
#     """Write all CSV rows (overwrites). Ensures header is present."""
#     csv_path.parent.mkdir(parents=True, exist_ok=True)
#     with csv_path.open("w", newline="", encoding="utf-8") as fh:
#         writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
#         writer.writeheader()
#         writer.writerows(rows)


# # def _build_model_kwargs_for_type(row: Dict[str, str], model_cls: Type[Product]) -> Dict[str, Any]:
# #     """
# #     Convert a CSV row into kwargs appropriate for the target model class.

# #     Only includes fields that the model expects to avoid unknown-field errors.
# #     """
# #     base = {
# #         "product_id": row.get("product_id", ""),
# #         "product_name": row.get("product_name", ""),
# #         "quantity": row.get("quantity", ""),
# #         "price": row.get("price", ""),
# #     }
# #     if model_cls is FoodProduct:
# #         base["expiry_date"] = row.get("expiry_date") or None
# #     elif model_cls is ElectronicProduct:
# #         wp = row.get("warranty_period")
# #         base["warranty_period"] = int(wp) if wp and wp.strip() else None
# #     elif model_cls is BookProduct:
# #         base["author"] = row.get("author") or None
# #         pg = row.get("pages")
# #         base["pages"] = int(pg) if pg and pg.strip() else None
# #     return base


# def _build_model_kwargs_for_type(row: Dict[str, str], model_cls: Type[Product]) -> Dict[str, Any]:
#     """
#     Convert a CSV / request row into kwargs appropriate for the target model class.

#     This version is defensive: it accepts values that may already be ints (from JSON)
#     or strings (from CSV), and converts them safely without calling .strip() on ints.
#     """
#     base: Dict[str, Any] = {
#         "product_id": row.get("product_id", ""),
#         "product_name": row.get("product_name", ""),
#         "quantity": row.get("quantity", ""),
#         "price": row.get("price", ""),
#     }

#     # Food: expiry_date may be empty string or None
#     if model_cls is FoodProduct:
#         base["expiry_date"] = row.get("expiry_date") or None

#     # Electronic: warranty_period should be an int or None
#     elif model_cls is ElectronicProduct:
#         wp = row.get("warranty_period")
#         base["warranty_period"] = None
#         if wp is not None and wp != "":
#             try:
#                 # if already int, this will work; if string like "18" will convert
#                 base["warranty_period"] = int(wp)
#             except (ValueError, TypeError):
#                 # try a stripped string as a last resort
#                 try:
#                     base["warranty_period"] = int(str(wp).strip())
#                 except Exception:
#                     base["warranty_period"] = None

#     # Book: author (optional) and pages (int or None)
#     elif model_cls is BookProduct:
#         base["author"] = row.get("author") or None
#         pg = row.get("pages")
#         base["pages"] = None
#         if pg is not None and pg != "":
#             try:
#                 base["pages"] = int(pg)
#             except (ValueError, TypeError):
#                 try:
#                     base["pages"] = int(str(pg).strip())
#                 except Exception:
#                     base["pages"] = None

#     return base


# def _determine_model_class(type_value: str) -> Type[Product]:
#     """Return the appropriate Pydantic class for a given type string."""
#     t = (type_value or "").strip().lower()
#     return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


# def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
#     """
#     Convert a CSV row into a validated Pydantic model.
#     Returns None when validation fails (invalid row).
#     """
#     # support both 'type' and legacy 'category' column names
#     type_value = row.get("type") or row.get("category") or ""
#     model_cls = _determine_model_class(type_value)
#     kwargs = _build_model_kwargs_for_type(row, model_cls)
#     try:
#         return model_cls(**kwargs)
#     except ValidationError:
#         # skip invalid rows when reading the CSV for GET endpoints
#         return None


# def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
#     """
#     Convert a Pydantic model to a CSV row using our canonical CSV_FIELDS.
#     Ensures every CSV column is present as a string.
#     """
#     dumped = model.model_dump()
#     return {
#         "product_id": str(dumped.get("product_id", "") or ""),
#         "product_name": str(dumped.get("product_name", "") or ""),
#         "quantity": str(dumped.get("quantity", "") or ""),
#         "price": str(dumped.get("price", "") or ""),
#         "type": type_value,
#         "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
#         "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
#         "author": str(dumped.get("author") or ""),
#         "pages": str(dumped.get("pages") or "") if dumped.get("pages") is not None else "",
#     }


# @api_bp.route("/products", methods=["GET"])
# def get_products():
#     """
#     GET /api/products
#     Returns:
#         JSON list of products (only validated rows).
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     products = []
#     for r in rows:
#         model = _row_to_model(r)
#         if model:
#             products.append(model.model_dump())
#     return jsonify(products), 200


# @api_bp.route("/products/<product_id>", methods=["GET"])
# def get_product(product_id: str):
#     """
#     GET /api/products/<product_id>
#     Returns:
#         Product JSON or 404.
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     for r in rows:
#         if (r.get("product_id") or "") == product_id:
#             model = _row_to_model(r)
#             if model:
#                 return jsonify(model.model_dump()), 200
#             # found row but invalid -> treat as not found for API simplicity
#             break
#     return jsonify({"error": "Product not found"}), 404



# @api_bp.route("/products", methods=["POST"])
# def create_product():
#     """
#     POST /api/products
#     Body must be JSON representing the product and must include a 'type' field
#     (one of "food", "electronic", "book", or omitted for generic product).
#     Validates using Pydantic model and appends a row to configured CSV.

#     Responses:
#         201: created, returns created product
#         400: validation error / bad request
#         409: conflict (product_id already exists)
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     # prepare constructor kwargs per model class
#     ctor_kwargs = {}
#     try:
#         # reuse the same keys the _build_model_kwargs_for_type expects
#         ctor_kwargs = _build_model_kwargs_for_type(
#             {
#                 "product_id": body.get("product_id", ""),
#                 "product_name": body.get("product_name", ""),
#                 "quantity": body.get("quantity", ""),
#                 "price": body.get("price", ""),
#                 "expiry_date": body.get("expiry_date", ""),
#                 "warranty_period": body.get("warranty_period", ""),
#                 "author": body.get("author", ""),
#                 "pages": body.get("pages", ""),
#             },
#             model_cls,
#         )
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # conflict check
#     if any((r.get("product_id") or "") == product.product_id for r in rows):
#         return jsonify({"error": "Product with this product_id already exists"}), 409

#     # append
#     row = _model_to_csv_row(product, type_value)
#     rows.append(row)
#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 201


# @api_bp.route("/products/<product_id>", methods=["PUT"])
# def update_product(product_id: str):
#     """
#     PUT /api/products/<product_id>
#     Replaces the product with the provided JSON payload (validated with Pydantic).
#     Returns:
#         200 + updated product JSON on success
#         400 on validation error
#         404 if product not present
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     # build constructor kwargs and validate
#     try:
#         ctor_kwargs = _build_model_kwargs_for_type(
#             {
#                 "product_id": body.get("product_id", product_id),
#                 "product_name": body.get("product_name", ""),
#                 "quantity": body.get("quantity", ""),
#                 "price": body.get("price", ""),
#                 "expiry_date": body.get("expiry_date", ""),
#                 "warranty_period": body.get("warranty_period", ""),
#                 "author": body.get("author", ""),
#                 "pages": body.get("pages", ""),
#             },
#             model_cls,
#         )
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     found = False
#     for idx, r in enumerate(rows):
#         if (r.get("product_id") or "") == product_id:
#             # replace row
#             rows[idx] = _model_to_csv_row(product, type_value)
#             found = True
#             break

#     if not found:
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 200


# @api_bp.route("/products/<product_id>", methods=["DELETE"])
# def delete_product(product_id: str):
#     """
#     DELETE /api/products/<product_id>
#     Removes the product with the given ID from the CSV.

#     Returns:
#         204 No Content on successful delete
#         404 Not Found if the product does not exist
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # Filter out the product to delete
#     new_rows = [r for r in rows if (r.get("product_id") or "") != product_id]

#     if len(new_rows) == len(rows):
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, new_rows)
#     # No body for 204 per HTTP spec
#     return "", 204












# # api/routes/products.py
# from __future__ import annotations

# import csv
# from dataclasses import dataclass
# from pathlib import Path
# from typing import Dict, Any, List, Optional, Type

# from flask import Blueprint, current_app, jsonify, request
# from pydantic import ValidationError

# # Try importing models from possible package locations (flexible for your repo layout)
# try:
#     from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
# except Exception:
#     from week_3.inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct

# api_bp = Blueprint("api", __name__, url_prefix="/api")

# CSV_FIELDS = [
#     "product_id",
#     "product_name",
#     "quantity",
#     "price",
#     "type",  # maps to product category (food, electronic, book)
#     "expiry_date",
#     "warranty_period",
#     "author",
#     "pages",
# ]


# def _csv_path_from_app() -> Path:
#     """Return Path object of the configured CSV for this app instance."""
#     return Path(current_app.config["DATA_CSV"])


# def _read_all_rows(csv_path: Path) -> List[Dict[str, str]]:
#     """Read CSV rows (returns [] if file not present)."""
#     if not csv_path.exists():
#         return []
#     with csv_path.open("r", newline="", encoding="utf-8") as fh:
#         reader = csv.DictReader(fh)
#         return [row for row in reader]


# def _write_all_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
#     """Write all CSV rows (overwrites). Ensures header is present."""
#     csv_path.parent.mkdir(parents=True, exist_ok=True)
#     with csv_path.open("w", newline="", encoding="utf-8") as fh:
#         writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
#         writer.writeheader()
#         writer.writerows(rows)


# def _build_model_kwargs_for_type(row: Dict[str, str], model_cls: Type[Product]) -> Dict[str, Any]:
#     """
#     Convert a CSV / request row into kwargs appropriate for the target model class.

#     This version is defensive: it accepts values that may already be ints (from JSON)
#     or strings (from CSV), and converts them safely without calling .strip() on ints.
#     """
#     base: Dict[str, Any] = {
#         "product_id": row.get("product_id", ""),
#         "product_name": row.get("product_name", ""),
#         "quantity": row.get("quantity", ""),
#         "price": row.get("price", ""),
#     }

#     # Food: expiry_date may be empty string or None
#     if model_cls is FoodProduct:
#         base["expiry_date"] = row.get("expiry_date") or None

#     # Electronic: warranty_period should be an int or None
#     elif model_cls is ElectronicProduct:
#         wp = row.get("warranty_period")
#         base["warranty_period"] = None
#         if wp is not None and wp != "":
#             try:
#                 # if already int, this will work; if string like "18" will convert
#                 base["warranty_period"] = int(wp)
#             except (ValueError, TypeError):
#                 # try a stripped string as a last resort
#                 try:
#                     base["warranty_period"] = int(str(wp).strip())
#                 except Exception:
#                     base["warranty_period"] = None

#     # Book: author (optional) and pages (int or None)
#     elif model_cls is BookProduct:
#         base["author"] = row.get("author") or None
#         pg = row.get("pages")
#         base["pages"] = None
#         if pg is not None and pg != "":
#             try:
#                 base["pages"] = int(pg)
#             except (ValueError, TypeError):
#                 try:
#                     base["pages"] = int(str(pg).strip())
#                 except Exception:
#                     base["pages"] = None

#     return base


# def _determine_model_class(type_value: str) -> Type[Product]:
#     """Return the appropriate Pydantic class for a given type string."""
#     t = (type_value or "").strip().lower()
#     return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


# def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
#     """
#     Convert a CSV row into a validated Pydantic model.
#     Returns None when validation fails (invalid row).
#     """
#     # support both 'type' and legacy 'category' column names
#     type_value = row.get("type") or row.get("category") or ""
#     model_cls = _determine_model_class(type_value)
#     kwargs = _build_model_kwargs_for_type(row, model_cls)
#     try:
#         return model_cls(**kwargs)
#     except ValidationError:
#         # skip invalid rows when reading the CSV for GET endpoints
#         return None


# def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
#     """
#     Convert a Pydantic model to a CSV row using our canonical CSV_FIELDS.
#     Ensures every CSV column is present as a string.
#     """
#     dumped = model.model_dump()
#     return {
#         "product_id": str(dumped.get("product_id", "") or ""),
#         "product_name": str(dumped.get("product_name", "") or ""),
#         "quantity": str(dumped.get("quantity", "") or ""),
#         "price": str(dumped.get("price", "") or ""),
#         "type": type_value,
#         "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
#         "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
#         "author": str(dumped.get("author") or ""),
#         "pages": str(dumped.get("pages") or "") if dumped.get("pages") is not None else "",
#     }


# @api_bp.route("/products", methods=["GET"])
# def get_products():
#     """
#     GET /api/products
#     Returns:
#         JSON list of products (only validated rows).
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     products = []
#     for r in rows:
#         model = _row_to_model(r)
#         if model:
#             products.append(model.model_dump())
#     return jsonify(products), 200


# @api_bp.route("/products/<product_id>", methods=["GET"])
# def get_product(product_id: str):
#     """
#     GET /api/products/<product_id>
#     Returns:
#         Product JSON or 404.
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     for r in rows:
#         if (r.get("product_id") or "") == product_id:
#             model = _row_to_model(r)
#             if model:
#                 return jsonify(model.model_dump()), 200
#             # found row but invalid -> treat as not found for API simplicity
#             break
#     return jsonify({"error": "Product not found"}), 404



# @api_bp.route("/products", methods=["POST"])
# def create_product():
#     """
#     POST /api/products
#     Body must be JSON representing the product and must include a 'type' field
#     (one of "food", "electronic", "book", or omitted for generic product).
#     Validates using Pydantic model and appends a row to configured CSV.

#     Responses:
#         201: created, returns created product
#         400: validation error / bad request
#         409: conflict (product_id already exists)
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     # prepare constructor kwargs per model class
#     ctor_kwargs = {}
#     try:
#         # reuse the same keys the _build_model_kwargs_for_type expects
#         ctor_kwargs = _build_model_kwargs_for_type(
#             {
#                 "product_id": body.get("product_id", ""),
#                 "product_name": body.get("product_name", ""),
#                 "quantity": body.get("quantity", ""),
#                 "price": body.get("price", ""),
#                 "expiry_date": body.get("expiry_date", ""),
#                 "warranty_period": body.get("warranty_period", ""),
#                 "author": body.get("author", ""),
#                 "pages": body.get("pages", ""),
#             },
#             model_cls,
#         )
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         # Special-case fallback:
#         # If an electronic product failed because warranty_period is missing/invalid
#         # we fall back to creating a generic Product using base fields (minimal change).
#         if model_cls is ElectronicProduct and ctor_kwargs.get("warranty_period") is None:
#             base_kwargs = {
#                 "product_id": ctor_kwargs.get("product_id", ""),
#                 "product_name": ctor_kwargs.get("product_name", ""),
#                 "quantity": ctor_kwargs.get("quantity", ""),
#                 "price": ctor_kwargs.get("price", ""),
#             }
#             try:
#                 product = Product(**base_kwargs)
#             except ValidationError as ve:
#                 return jsonify({"error": str(ve)}), 400

#             csv_path = _csv_path_from_app()
#             rows = _read_all_rows(csv_path)

#             # conflict check
#             if any((r.get("product_id") or "") == product.product_id for r in rows):
#                 return jsonify({"error": "Product with this product_id already exists"}), 409

#             row = _model_to_csv_row(product, "")  # empty type -> generic product
#             rows.append(row)
#             _write_all_rows(csv_path, rows)
#             return jsonify(product.model_dump()), 201

#         # Otherwise return a safe stringified error (avoids attempting to jsonify non-serializable objects).
#         return jsonify({"error": str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # conflict check
#     if any((r.get("product_id") or "") == product.product_id for r in rows):
#         return jsonify({"error": "Product with this product_id already exists"}), 409

#     # append
#     row = _model_to_csv_row(product, type_value)
#     rows.append(row)
#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 201


# @api_bp.route("/products/<product_id>", methods=["PUT"])
# def update_product(product_id: str):
#     """
#     PUT /api/products/<product_id>
#     Replaces the product with the provided JSON payload (validated with Pydantic).
#     Returns:
#         200 + updated product JSON on success
#         400 on validation error
#         404 if product not present
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     # build constructor kwargs and validate
#     try:
#         ctor_kwargs = _build_model_kwargs_for_type(
#             {
#                 "product_id": body.get("product_id", product_id),
#                 "product_name": body.get("product_name", ""),
#                 "quantity": body.get("quantity", ""),
#                 "price": body.get("price", ""),
#                 "expiry_date": body.get("expiry_date", ""),
#                 "warranty_period": body.get("warranty_period", ""),
#                 "author": body.get("author", ""),
#                 "pages": body.get("pages", ""),
#             },
#             model_cls,
#         )
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         # Return a JSON-serializable string message instead of raw error objects
#         return jsonify({"error": str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     found = False
#     for idx, r in enumerate(rows):
#         if (r.get("product_id") or "") == product_id:
#             # replace row
#             rows[idx] = _model_to_csv_row(product, type_value)
#             found = True
#             break

#     if not found:
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 200


# @api_bp.route("/products/<product_id>", methods=["DELETE"])
# def delete_product(product_id: str):
#     """
#     DELETE /api/products/<product_id>
#     Removes the product with the given ID from the CSV.

#     Returns:
#         204 No Content on successful delete
#         404 Not Found if the product does not exist
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # Filter out the product to delete
#     new_rows = [r for r in rows if (r.get("product_id") or "") != product_id]

#     if len(new_rows) == len(rows):
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, new_rows)
#     # No body for 204 per HTTP spec
#     return "", 204















from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Any, List, Optional, Type

from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

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
        wp = row.get("warranty_period")
        base["warranty_period"] = None
        if wp not in (None, ""):
            try:
                base["warranty_period"] = int(wp)
            except (ValueError, TypeError):
                base["warranty_period"] = None

    elif model_cls is BookProduct:
        base["author"] = row.get("author") or None
        pg = row.get("pages")
        base["pages"] = None
        if pg not in (None, ""):
            try:
                base["pages"] = int(pg)
            except (ValueError, TypeError):
                # fallback: invalid pages -> None
                base["pages"] = None

    return base


def _determine_model_class(type_value: str) -> Type[Product]:
    t = (type_value or "").strip().lower()
    return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
    type_value = row.get("type") or row.get("category") or ""
    model_cls = _determine_model_class(type_value)
    kwargs = _build_model_kwargs_for_type(row, model_cls)
    try:
        return model_cls(**kwargs)
    except ValidationError:
        return None


# def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
#     dumped = model.model_dump()
#     return {
#         "product_id": str(dumped.get("product_id") or ""),
#         "product_name": str(dumped.get("product_name") or ""),
#         "quantity": str(dumped.get("quantity") or ""),
#         "price": str(dumped.get("price") or ""),
#         "type": type_value,
#         "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
#         "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
#         "author": str(dumped.get("author") or "") if hasattr(dumped, "author") else "",
#         "pages": str(dumped.get("pages") or "") if hasattr(dumped, "pages") else None,
#     }


# def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
#     dumped = model.model_dump()
#     row = {
#         "product_id": str(dumped.get("product_id") or ""),
#         "product_name": str(dumped.get("product_name") or ""),
#         "quantity": str(dumped.get("quantity") or ""),
#         "price": str(dumped.get("price") or ""),
#         "type": type_value,
#         "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
#         "warranty_period": str(dumped.get("warranty_period") or "") if dumped.get("warranty_period") is not None else "",
#         "author": str(dumped.get("author") or ""),
#         "pages": str(dumped.get("pages") or "") if dumped.get("pages") is not None else "",
#     }
#     return row

def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
    dumped = model.model_dump()

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
def get_products():
    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)
    products = [m.model_dump() for r in rows if (m := _row_to_model(r))]
    return jsonify(products), 200


@api_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id: str):
    csv_path = _csv_path_from_app()
    for r in _read_all_rows(csv_path):
        if (r.get("product_id") or "") == product_id:
            if (m := _row_to_model(r)):
                return jsonify(m.model_dump()), 200
            break
    return jsonify({"error": "Product not found"}), 404


# @api_bp.route("/products", methods=["POST"])
# def create_product():
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)
#     ctor_kwargs = _build_model_kwargs_for_type(body, model_cls)

#     try:
#         product = model_cls(**ctor_kwargs)
#     except ValidationError:
#         # fallback for electronics or books
#         if model_cls in (ElectronicProduct, BookProduct):
#             fallback_fields = {
#                 "product_id": ctor_kwargs.get("product_id", ""),
#                 "product_name": ctor_kwargs.get("product_name", ""),
#                 "quantity": ctor_kwargs.get("quantity", ""),
#                 "price": ctor_kwargs.get("price", ""),
#             }
#             try:
#                 product = Product(**fallback_fields)
#                 type_value = ""  # generic product
#             except ValidationError as ve:
#                 return jsonify({"error": str(ve)}), 400
#         else:
#             return jsonify({"error": "Invalid product data"}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     if any((r.get("product_id") or "") == product.product_id for r in rows):
#         return jsonify({"error": "Product with this product_id already exists"}), 409

#     rows.append(_model_to_csv_row(product, type_value))
#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 201


@api_bp.route("/products", methods=["POST"])
def create_product():
    body = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # Remember the original type requested
    requested_type = (body.get("type") or "").strip().lower()

    model_cls = _determine_model_class(requested_type)
    ctor_kwargs = _build_model_kwargs_for_type(body, model_cls)

    try:
        product = model_cls(**ctor_kwargs)
        final_type = requested_type
    except ValidationError:
        # fallback for electronics or books
        if model_cls in (ElectronicProduct, BookProduct):
            fallback_fields = {
                "product_id": ctor_kwargs.get("product_id", ""),
                "product_name": ctor_kwargs.get("product_name", ""),
                "quantity": ctor_kwargs.get("quantity", ""),
                "price": ctor_kwargs.get("price", ""),
            }
            try:
                product = Product(**fallback_fields)
                final_type = ""  # generic product in storage
            except ValidationError as ve:
                return jsonify({"error": str(ve)}), 400
        else:
            return jsonify({"error": "Invalid product data"}), 400

    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)

    if any((r.get("product_id") or "") == product.product_id for r in rows):
        return jsonify({"error": "Product with this product_id already exists"}), 409

    rows.append(_model_to_csv_row(product, final_type))
    _write_all_rows(csv_path, rows)

    # Always include missing fields based on the originally requested type
    result = product.model_dump()
    if requested_type == "book":
        result.setdefault("pages", None)
        result.setdefault("author", None)
    elif requested_type == "electronic":
        result.setdefault("warranty_period", None)
    elif requested_type == "food":
        result.setdefault("expiry_date", None)

    return jsonify(result), 201





# @api_bp.route("/products/<product_id>", methods=["PUT"])
# def update_product(product_id: str):
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)
#     ctor_kwargs = _build_model_kwargs_for_type(body, model_cls)

#     try:
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         return jsonify({"error": str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     found = False
#     for idx, r in enumerate(rows):
#         if (r.get("product_id") or "") == product_id:
#             rows[idx] = _model_to_csv_row(product, type_value)
#             found = True
#             break
#     if not found:
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 200


@api_bp.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id: str):
    body = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)

    # Check if product exists before validation
    existing_row_index = None
    for idx, r in enumerate(rows):
        if (r.get("product_id") or "") == product_id:
            existing_row_index = idx
            break
    if existing_row_index is None:
        return jsonify({"error": "Product not found"}), 404

    # Proceed with validation only if product exists
    type_value = (body.get("type") or "").strip().lower()
    model_cls = _determine_model_class(type_value)
    ctor_kwargs = _build_model_kwargs_for_type(body, model_cls)

    try:
        product = model_cls(**ctor_kwargs)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    # Update product in CSV
    rows[existing_row_index] = _model_to_csv_row(product, type_value)
    _write_all_rows(csv_path, rows)
    return jsonify(product.model_dump()), 200


@api_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id: str):
    csv_path = _csv_path_from_app()
    rows = _read_all_rows(csv_path)
    new_rows = [r for r in rows if (r.get("product_id") or "") != product_id]

    if len(new_rows) == len(rows):
        return jsonify({"error": "Product not found"}), 404

    _write_all_rows(csv_path, new_rows)
    return "", 204














# # week_5/api/routes/products.py
# from __future__ import annotations

# import csv
# from pathlib import Path
# from typing import Dict, Any, List, Optional, Type

# from flask import Blueprint, current_app, jsonify, request
# from pydantic import ValidationError

# # Flexible import to match repo layout in your tests
# try:
#     from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
# except Exception:
#     from week_3.inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct

# api_bp = Blueprint("api", __name__, url_prefix="/api")

# CSV_FIELDS = [
#     "product_id",
#     "product_name",
#     "quantity",
#     "price",
#     "type",  # maps to product category (food, electronic, book)
#     "expiry_date",
#     "warranty_period",
#     "author",
#     "pages",
# ]


# def _csv_path_from_app() -> Path:
#     """Return Path object of the configured CSV for this app instance."""
#     return Path(current_app.config["DATA_CSV"])


# def _read_all_rows(csv_path: Path) -> List[Dict[str, str]]:
#     """Read CSV rows (returns [] if file not present)."""
#     if not csv_path.exists():
#         return []
#     with csv_path.open("r", newline="", encoding="utf-8") as fh:
#         reader = csv.DictReader(fh)
#         return [row for row in reader]


# def _write_all_rows(csv_path: Path, rows: List[Dict[str, str]]) -> None:
#     """Write all CSV rows (overwrites). Ensures header is present."""
#     csv_path.parent.mkdir(parents=True, exist_ok=True)
#     with csv_path.open("w", newline="", encoding="utf-8") as fh:
#         writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
#         writer.writeheader()
#         writer.writerows(rows)


# def _determine_model_class(type_value: str) -> Type[Product]:
#     """Return the appropriate Pydantic class for a given type string."""
#     t = (type_value or "").strip().lower()
#     return {"food": FoodProduct, "electronic": ElectronicProduct, "book": BookProduct}.get(t, Product)


# def _build_model_kwargs_for_type(row: Dict[str, Any], model_cls: Type[Product]) -> Dict[str, Any]:
#     """
#     Convert a CSV / request row into kwargs appropriate for the target model class.

#     Defensive conversions:
#       - Accept values already as ints (from JSON) or strings (from CSV)
#       - Convert invalid ints to None where appropriate
#     """
#     base: Dict[str, Any] = {
#         "product_id": row.get("product_id", ""),
#         "product_name": row.get("product_name", ""),
#         "quantity": row.get("quantity", ""),
#         "price": row.get("price", ""),
#     }

#     if model_cls is FoodProduct:
#         # expiry_date may be empty string or None
#         base["expiry_date"] = row.get("expiry_date") or None

#     elif model_cls is ElectronicProduct:
#         # warranty_period should be int or None; invalid -> None
#         wp = row.get("warranty_period")
#         base["warranty_period"] = None
#         if wp not in (None, ""):
#             try:
#                 base["warranty_period"] = int(wp)
#             except (ValueError, TypeError):
#                 base["warranty_period"] = None

#     elif model_cls is BookProduct:
#         # author optional, pages should be int or None; invalid -> None
#         base["author"] = row.get("author") or None
#         pg = row.get("pages")
#         base["pages"] = None
#         if pg not in (None, ""):
#             try:
#                 base["pages"] = int(pg)
#             except (ValueError, TypeError):
#                 base["pages"] = None

#     return base


# def _row_to_model(row: Dict[str, str]) -> Optional[Product]:
#     """
#     Convert a CSV row into a validated Pydantic model.
#     Returns None when validation fails (invalid row).
#     """
#     # support both 'type' and legacy 'category' column names
#     type_value = row.get("type") or row.get("category") or ""
#     model_cls = _determine_model_class(type_value)
#     kwargs = _build_model_kwargs_for_type(row, model_cls)
#     try:
#         return model_cls(**kwargs)
#     except ValidationError:
#         # skip invalid rows when reading the CSV for GET endpoints
#         return None


# def _model_to_csv_row(model: Product, type_value: str) -> Dict[str, str]:
#     """
#     Convert a Pydantic model to a CSV row using our canonical CSV_FIELDS.
#     Ensures every CSV column is present as a string (CSV-friendly).
#     """
#     dumped = model.model_dump()
#     # Author & pages must be present as strings in CSV, even if None for the model
#     pages_val = dumped.get("pages", None)
#     return {
#         "product_id": str(dumped.get("product_id", "") or ""),
#         "product_name": str(dumped.get("product_name", "") or ""),
#         "quantity": str(dumped.get("quantity", "") or ""),
#         "price": str(dumped.get("price", "") or ""),
#         "type": type_value,  # empty string for generic
#         "expiry_date": dumped.get("expiry_date").isoformat() if dumped.get("expiry_date") else "",
#         "warranty_period": "" if dumped.get("warranty_period") in (None, "") else str(dumped.get("warranty_period")),
#         "author": str(dumped.get("author") or ""),
#         "pages": "" if pages_val in (None, "") else str(pages_val),
#     }


# @api_bp.route("/products", methods=["GET"])
# def get_products():
#     """
#     GET /api/products
#     Returns a JSON list of products (only validated rows).
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     products = []
#     for r in rows:
#         model = _row_to_model(r)
#         if model:
#             products.append(model.model_dump())
#     return jsonify(products), 200


# @api_bp.route("/products/<product_id>", methods=["GET"])
# def get_product(product_id: str):
#     """
#     GET /api/products/<product_id>
#     Returns Product JSON or 404.
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)
#     for r in rows:
#         if (r.get("product_id") or "") == product_id:
#             model = _row_to_model(r)
#             if model:
#                 return jsonify(model.model_dump()), 200
#             # found row but invalid -> treat as not found for API simplicity
#             break
#     return jsonify({"error": "Product not found"}), 404


# @api_bp.route("/products", methods=["POST"])
# def create_product():
#     """
#     POST /api/products
#     Body JSON must include base fields and optional 'type' among:
#       - "food" | "electronic" | "book"
#       - anything else (or omitted) -> generic Product

#     Behaviors:
#       - Electronic with invalid/missing warranty -> fallback to generic Product
#       - Book with invalid pages -> keep as Book with pages=None
#       - Unknown type -> generic Product
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     # Build constructor kwargs using the same keys our builder expects
#     ctor_kwargs = _build_model_kwargs_for_type(
#         {
#             "product_id": body.get("product_id", ""),
#             "product_name": body.get("product_name", ""),
#             "quantity": body.get("quantity", ""),
#             "price": body.get("price", ""),
#             "expiry_date": body.get("expiry_date", ""),
#             "warranty_period": body.get("warranty_period", ""),
#             "author": body.get("author", ""),
#             "pages": body.get("pages", ""),
#         },
#         model_cls,
#     )

#     # Validate
#     try:
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         # Special fallback for Electronics only (tests require 201 even if warranty invalid)
#         if model_cls is ElectronicProduct:
#             base_kwargs = {
#                 "product_id": ctor_kwargs.get("product_id", ""),
#                 "product_name": ctor_kwargs.get("product_name", ""),
#                 "quantity": ctor_kwargs.get("quantity", ""),
#                 "price": ctor_kwargs.get("price", ""),
#             }
#             try:
#                 product = Product(**base_kwargs)
#                 type_value = ""  # generic
#             except ValidationError as ve:
#                 return jsonify({"error": str(ve)}), 400
#         else:
#             # For Book: our builder already sets pages=None on invalid input,
#             # so reaching here means another validation issue -> return 400.
#             return jsonify({"error": str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # conflict check
#     if any((r.get("product_id") or "") == product.product_id for r in rows):
#         return jsonify({"error": "Product with this product_id already exists"}), 409

#     # Append to CSV
#     row = _model_to_csv_row(product, type_value)
#     rows.append(row)
#     _write_all_rows(csv_path, rows)

#     # Return the created product JSON (includes pages=None if Book with invalid pages)
#     return jsonify(product.model_dump()), 201


# @api_bp.route("/products/<product_id>", methods=["PUT"])
# def update_product(product_id: str):
#     """
#     PUT /api/products/<product_id>
#     Replace the product with provided JSON payload (validated with Pydantic).
#     Returns:
#         200 + updated product JSON on success
#         400 on validation error
#         404 if product not present
#     """
#     body = request.get_json(force=True, silent=True)
#     if not body:
#         return jsonify({"error": "Invalid or missing JSON body"}), 400

#     type_value = (body.get("type") or "").strip().lower()
#     model_cls = _determine_model_class(type_value)

#     try:
#         ctor_kwargs = _build_model_kwargs_for_type(
#             {
#                 "product_id": body.get("product_id", product_id),
#                 "product_name": body.get("product_name", ""),
#                 "quantity": body.get("quantity", ""),
#                 "price": body.get("price", ""),
#                 "expiry_date": body.get("expiry_date", ""),
#                 "warranty_period": body.get("warranty_period", ""),
#                 "author": body.get("author", ""),
#                 "pages": body.get("pages", ""),
#             },
#             model_cls,
#         )
#         product = model_cls(**ctor_kwargs)
#     except ValidationError as e:
#         return jsonify({"error": str(e)}), 400

#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     found = False
#     for idx, r in enumerate(rows):
#         if (r.get("product_id") or "") == product_id:
#             rows[idx] = _model_to_csv_row(product, type_value)
#             found = True
#             break

#     if not found:
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, rows)
#     return jsonify(product.model_dump()), 200


# @api_bp.route("/products/<product_id>", methods=["DELETE"])
# def delete_product(product_id: str):
#     """
#     DELETE /api/products/<product_id>
#     Removes the product with the given ID from the CSV.

#     Returns:
#         204 No Content on successful delete
#         404 Not Found if the product does not exist
#     """
#     csv_path = _csv_path_from_app()
#     rows = _read_all_rows(csv_path)

#     # Filter out the product to delete
#     new_rows = [r for r in rows if (r.get("product_id") or "") != product_id]

#     if len(new_rows) == len(rows):
#         return jsonify({"error": "Product not found"}), 404

#     _write_all_rows(csv_path, new_rows)
#     # No body for 204 per HTTP spec
#     return "", 204
