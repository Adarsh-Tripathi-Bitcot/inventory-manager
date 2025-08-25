"""Pydantic request models for the Inventory API."""

from __future__ import annotations
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class ProductBaseRequest(BaseModel):
    """Base schema shared by all product types."""

    product_id: int = Field(..., gt=0, description="Unique positive integer external ID")
    product_name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., ge=0, description="Quantity in stock")
    price: float = Field(..., gt=0, description="Price of the product")
    type: Optional[str] = Field("", description="Type of product: food, electronic, book or generic")

    model_config = ConfigDict(extra="forbid")


class FoodProductCreate(ProductBaseRequest):
    """Schema for creating a food product."""
    type: str = "food"
    expiry_date: date = Field(..., description="Expiry date in YYYY-MM-DD format")

    model_config = ConfigDict(extra="forbid")


class ElectronicProductCreate(ProductBaseRequest):
    """Schema for creating an electronic product."""
    type: str = "electronic"
    warranty_period: int = Field(..., gt=0, description="Warranty period in months")

    model_config = ConfigDict(extra="forbid")


class BookProductCreate(ProductBaseRequest):
    """Schema for creating a book product."""
    type: str = "book"
    author: str = Field(..., description="Book author")
    pages: int = Field(..., ge=1, description="Total pages")

    model_config = ConfigDict(extra="forbid")


class GenericProductCreate(ProductBaseRequest):
    """Schema for creating a generic product."""
    type: str = ""


class ProductUpdate(BaseModel):
    """Schema for updating a product (partial updates allowed)."""
    product_name: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    type: Optional[str] = None
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = Field(None, ge=0)
    author: Optional[str] = None
    pages: Optional[int] = Field(None, ge=1)

    model_config = ConfigDict(extra="forbid")
    