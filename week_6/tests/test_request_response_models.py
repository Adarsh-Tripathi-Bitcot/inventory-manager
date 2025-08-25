"""Tests for Pydantic request and response models."""

from datetime import date
import pytest
from pydantic import ValidationError
from week_6.api.request_model import FoodProductCreate, ProductUpdate
from week_6.api.response_model import ProductResponse


def test_food_product_create_valid() -> None:
    """Valid FoodProductCreate instance passes validation."""
    f = FoodProductCreate(product_id=1, product_name="Apple", quantity=1, price=1.0, expiry_date=date.today())
    assert f.type == "food"
    assert f.quantity == 1


def test_product_update_partial() -> None:
    """Partial update allows unset fields."""
    u = ProductUpdate(product_name="New")
    assert u.product_name == "New"
    assert u.price is None


def test_invalid_food_missing_expiry() -> None:
    """Missing expiry_date raises ValidationError."""
    with pytest.raises(ValidationError) as exc:
        FoodProductCreate(product_id=1, product_name="Apple", quantity=1, price=1.0)
    assert "expiry_date" in str(exc.value)


def test_product_response_from_orm() -> None:
    """ProductResponse can be created from ORM-like object using from_attributes."""
    class Dummy:
        product_id = 1
        product_name = "X"
        quantity = 1
        price = 1.0
        type = "book"
        expiry_date = None
        warranty_period = None
        author = None
        pages = None

    resp = ProductResponse.model_validate(Dummy())
    assert resp.product_name == "X"
    assert resp.type == "book"