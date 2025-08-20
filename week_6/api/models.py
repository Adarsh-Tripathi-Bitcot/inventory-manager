"""Database models for the Inventory API."""

from datetime import date
from typing import Optional, Union
from .db import db
from sqlalchemy import CheckConstraint

class Product(db.Model):
    """SQLAlchemy model representing a product in the inventory."""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    warranty_period = db.Column(db.Integer, nullable=True)
    author = db.Column(db.String(256), nullable=True)
    pages = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('product_id > 0', name='check_product_id_positive'),
    )

    def __repr__(self) -> str:
        """String representation of the product."""
        return f"<Product {self.product_id} {self.product_name}>"

    def to_dict(self) -> dict[str, Union[str, int, float, None]]:
        """Convert product instance into a JSON-serializable dictionary.

        Returns:
            dict[str, str | int | float | None]: Dictionary representation of product.
        """
        return {
            "product_id": self.product_id,
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
