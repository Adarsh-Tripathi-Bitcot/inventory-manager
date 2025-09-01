"""Database models for the Inventory API."""

from datetime import date
from typing import Optional, Union, Dict
from .db import db
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    """SQLAlchemy model representing a product in the inventory."""

    __tablename__ = "products"

    product_id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name: str = db.Column(db.String(256), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    type: Optional[str] = db.Column(db.String(50), nullable=True)
    expiry_date: Optional[date] = db.Column(db.Date, nullable=True)
    warranty_period: Optional[int] = db.Column(db.Integer, nullable=True)
    author: Optional[str] = db.Column(db.String(256), nullable=True)
    pages: Optional[int] = db.Column(db.Integer, nullable=True)

    # New field to track ownership
    created_by = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="products")

    __table_args__ = (
        CheckConstraint('product_id > 0', name='check_product_id_positive'),
    )

    def __repr__(self) -> str:
        return f"<Product {self.product_id} {self.product_name}>"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "type": self.type or "",
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else "",
            "warranty_period": self.warranty_period,
            "author": self.author or "",
            "pages": self.pages,
            "created_by": self.created_by
        }

class RoleEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"

class User(db.Model):
    """SQLAlchemy model representing an application user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default=RoleEnum.STAFF.value, nullable=False)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the user's password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"