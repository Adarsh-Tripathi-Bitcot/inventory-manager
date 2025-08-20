"""Database models for the Inventory API."""

from datetime import date
from typing import Optional
from .db import db


class Product(db.Model):
    """SQLAlchemy model representing a product in the inventory.

    Attributes:
        id (int): Auto-incrementing primary key.
        product_id (str): External unique identifier for the product.
        product_name (str): Human-readable name of the product.
        quantity (int): Available stock quantity.
        price (float): Price of the product.
        type (Optional[str]): Product type ("food", "electronic", "book").
        expiry_date (Optional[date]): Expiry date (for food products).
        warranty_period (Optional[int]): Warranty period in months (for electronics).
        author (Optional[str]): Author name (for books).
        pages (Optional[int]): Number of pages (for books).
    """

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.String(64), unique=True, nullable=False
    )  # external id used in API URLs
    product_name = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    warranty_period = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(256), nullable=True)
    pages = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        """String representation of the product."""
        return f"<Product {self.product_id} {self.product_name}>"

    def to_dict(self) -> dict[str, str | int | float | None]:
        """Convert product instance into a JSON-serializable dictionary.

        Returns:
            dict[str, str | int | float | None]: Dictionary representation of product.
        """
        return {
            "product_id": str(self.product_id),
            "product_name": str(self.product_name),
            "quantity": self.quantity,
            "price": float(self.price),
            "type": self.type or "",
            "expiry_date": self.expiry_date.isoformat()
            if self.expiry_date is not None
            else "",
            "warranty_period": self.warranty_period
            if self.warranty_period is not None
            else None,
            "author": self.author if self.author is not None else "",
            "pages": self.pages if self.pages is not None else None,
        }
