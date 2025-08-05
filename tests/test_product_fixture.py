import pytest
from pydantic import ValidationError
from datetime import date
from inventory_manager.models import FoodProduct, ElectronicProduct, BookProduct

def test_product_total_value(base_product):
    total = base_product.get_total_value()
    assert total == 200.0

def test_valid_food_product(food_product):
    assert food_product.expiry_date == date(2025, 12, 31)

def test_invalid_food_product_missing_expiry():
    with pytest.raises(ValidationError) as exc_info:
        FoodProduct(
            product_id="F002",
            product_name="Milk",
            quantity=2,
            price=1.5,
            expiry_date=None
        )
    assert "expiry_date" in str(exc_info.value)

def test_valid_electronic_product(electronic_product):
    assert electronic_product.warranty_period == 24

def test_invalid_electronic_product_missing_warranty():
    with pytest.raises(ValidationError) as exc_info:
        ElectronicProduct(
            product_id="E002",
            product_name="Tablet",
            quantity=4,
            price=150.0,
            warranty_period=None
        )
    assert "warranty_period" in str(exc_info.value)

def test_valid_book_product(book_product):
    assert book_product.author == "John Doe"
    assert book_product.pages == 300

def test_invalid_book_product_missing_author():
    with pytest.raises(ValidationError) as exc_info:
        BookProduct(
            product_id="B002",
            product_name="C++ 101",
            quantity=4,
            price=12.0,
            author=None,
            pages=250
        )
    assert "author" in str(exc_info.value)

def test_invalid_book_product_missing_pages():
    with pytest.raises(ValidationError) as exc_info:
        BookProduct(
            product_id="B003",
            product_name="Go Basics",
            quantity=3,
            price=10.0,
            author="Alex",
            pages=None
        )
    assert "pages" in str(exc_info.value)
