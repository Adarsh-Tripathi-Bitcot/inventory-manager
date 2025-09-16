"""Tests for SQLAlchemy Product model (patched for created_by constraint)."""

from week_6_and_7.api.models import Product, User
from week_6_and_7.api.db import db


def test_product_repr_and_to_dict(db) -> None:
    """Test __repr__ and to_dict methods of Product."""
    # Create a user to satisfy Product.created_by NOT NULL FK
    u = User(username="owner1", role="staff")
    u.set_password("pw")
    db.session.add(u)
    db.session.commit()

    p = Product(
        product_id=1,
        product_name="Item",
        quantity=5,
        price=10.5,
        type="food",
        created_by=u.id,  # required
    )
    db.session.add(p)
    db.session.commit()

    assert "<Product 1 Item>" == repr(p)
    dct = p.to_dict()
    assert dct["product_name"] == "Item"
    assert isinstance(dct["price"], float)
    assert dct["expiry_date"] == ""
    assert dct["created_by"] == u.id
