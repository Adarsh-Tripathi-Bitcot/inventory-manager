"""Pydantic schemas for request/response validation in the Inventory API."""

from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


# --------------------
# Base Schemas
# --------------------
class ProductBase(BaseModel):
    """Base schema shared by all product types."""

    product_id: str = Field(..., description="Unique external ID of product")
    product_name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., ge=0, description="Quantity in stock")
    price: float = Field(..., gt=0, description="Price of the product")
    type: str = Field(
        "", description="Type of product: 'food', 'electronic', 'book' or '' (generic)"
    )


# --------------------
# Request Models (Create)
# --------------------
class FoodProductCreate(ProductBase):
    """Schema for creating a food product."""

    type: str = "food"
    expiry_date: date = Field(..., description="Expiry date in YYYY-MM-DD format")


class ElectronicProductCreate(ProductBase):
    """Schema for creating an electronic product."""

    type: str = "electronic"
    warranty_period: int = Field(..., gt=0, description="Warranty period in months")


class BookProductCreate(ProductBase):
    """Schema for creating a book product."""

    type: str = "book"
    author: str = Field(..., description="Author of the book")
    pages: int = Field(..., ge=1, description="Total number of pages")


class GenericProductCreate(ProductBase):
    """Schema for creating a generic product (no type-specific fields)."""

    type: str = ""


# --------------------
# Request Model (Update / PUT)
# --------------------
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


# --------------------
# Response Model
# --------------------
class ProductResponse(ProductBase):
    """Standard response model returned by API."""

    id: int
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None
    author: Optional[str] = None
    pages: Optional[int] = None

    class Config:
        """Configuration for ORM compatibility."""

        from_attributes = True
