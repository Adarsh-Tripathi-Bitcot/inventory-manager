"""Compatibility shim for request/response schemas.

This file re-exports request and response models so existing imports
(`from ..schemas import ...`) keep working without any code changes.

You may delete this file later **only after** updating all imports to use:
- `from .request_model import ...`
- `from .response_model import ProductResponse`
"""

from __future__ import annotations

# Request models
from .request_model import (
    ProductBaseRequest as ProductBase,
    FoodProductCreate,
    ElectronicProductCreate,
    BookProductCreate,
    GenericProductCreate,
    ProductUpdate,
)

# Response model
from .response_model import ProductResponse

__all__ = [
    "ProductBase",
    "FoodProductCreate",
    "ElectronicProductCreate",
    "BookProductCreate",
    "GenericProductCreate",
    "ProductUpdate",
    "ProductResponse",
]
