"""Tests for SQLAlchemy Product model."""

from week_6.api.models import Product
from week_6.api.db import db


def test_product_repr_and_to_dict(db) -> None:
    """Test __repr__ and to_dict methods of Product."""
    p = Product(
        product_id=1,
        product_name="Item",
        quantity=5,
        price=10.5,
        type="food",
    )
    db.session.add(p)
    db.session.commit()
    assert "<Product 1 Item>" == repr(p)
    dct = p.to_dict()
    assert dct["product_name"] == "Item"
    assert isinstance(dct["price"], float)
    assert dct["expiry_date"] == ""