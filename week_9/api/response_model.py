"""Pydantic response models for the Inventory API."""

from __future__ import annotations
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class ProductResponse(BaseModel):
    """Standard product response returned by API."""

    product_id: int = Field(..., gt=0)
    product_name: str
    quantity: int
    price: float 
    type: Optional[str] = Field("", description="food | electronic | book | ''")
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None
    author: Optional[str] = None
    pages: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
