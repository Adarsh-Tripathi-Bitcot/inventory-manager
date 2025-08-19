import pytest
from pydantic import ValidationError
from datetime import date
from inventory_manager.models import FoodProduct, ElectronicProduct, BookProduct


def test_product_total_value(base_product) -> None:
    """Test total value calculation for base Product fixture."""
    total = base_product.get_total_value()
    assert total == 200.0


def test_valid_food_product(food_product) -> None:
    """Test FoodProduct fixture for correct expiry date."""
    assert food_product.expiry_date == date(2025, 12, 31)


@pytest.mark.parametrize(
    "expiry_date", [None]
)
def test_invalid_food_product_missing_expiry(expiry_date) -> None:
    """
    Test FoodProduct with invalid expiry_date using parametrize.

    Args:
        expiry_date: Invalid expiry_date (None).
    """
    with pytest.raises(ValidationError) as exc_info:
        FoodProduct(
            product_id="F002",
            product_name="Milk",
            quantity=2,
            price=1.5,
            expiry_date=expiry_date,
        )
    assert "expiry_date" in str(exc_info.value)


def test_valid_electronic_product(electronic_product) -> None:
    """Test ElectronicProduct fixture for correct warranty period."""
    assert electronic_product.warranty_period == 24


@pytest.mark.parametrize(
    "warranty", [None]
)
def test_invalid_electronic_product_missing_warranty(warranty) -> None:
    """
    Test ElectronicProduct with missing warranty period.

    Args:
        warranty: Invalid warranty_period (None).
    """
    with pytest.raises(ValidationError) as exc_info:
        ElectronicProduct(
            product_id="E002",
            product_name="Tablet",
            quantity=4,
            price=150.0,
            warranty_period=warranty,
        )
    assert "warranty_period" in str(exc_info.value)


def test_valid_book_product(book_product) -> None:
    """Test BookProduct fixture for valid fields."""
    assert book_product.author == "John Doe"
    assert book_product.pages == 300


@pytest.mark.parametrize(
    "author, pages",
    [
        (None, 250),
        ("Alex", None),
    ],
)
def test_invalid_book_product_missing_fields(author: str | None, pages: int | None) -> None:
    """
    Parametrized test for BookProduct with missing author or pages.

    Args:
        author (str | None): Invalid author field.
        pages (int | None): Invalid pages field.
    """
    with pytest.raises(ValidationError) as exc_info:
        BookProduct(
            product_id="BXYZ",
            product_name="Some Book",
            quantity=3,
            price=20.0,
            author=author,
            pages=pages,
        )
    if author is None:
        assert "author" in str(exc_info.value)
    if pages is None:
        assert "pages" in str(exc_info.value)


def test_base_product_fixture(base_product) -> None:
    """Assert base_product fixture fields are valid."""
    assert base_product.product_id == "P001"
    assert base_product.product_name == "Generic Product"
    assert base_product.quantity == 10
    assert base_product.price == 20.0


def test_food_product_fixture(food_product) -> None:
    """Assert food_product fixture fields are valid."""
    assert food_product.product_id == "F001"
    assert food_product.product_name == "Bread"
    assert food_product.quantity == 5
    assert food_product.price == 2.5
    assert str(food_product.expiry_date) == "2025-12-31"


def test_electronic_product_fixture(electronic_product) -> None:
    """Assert electronic_product fixture fields are valid."""
    assert electronic_product.product_id == "E001"
    assert electronic_product.product_name == "Smartphone"
    assert electronic_product.quantity == 3
    assert electronic_product.price == 299.99
    assert electronic_product.warranty_period == 24


def test_book_product_fixture(book_product) -> None:
    """Assert book_product fixture fields are valid."""
    assert book_product.product_id == "B001"
    assert book_product.product_name == "Python 101"
    assert book_product.quantity == 7
    assert book_product.price == 15.0
    assert book_product.author == "John Doe"
    assert book_product.pages == 300


def test_valid_csv_file_fixture(valid_csv_file: str) -> None:
    """
    Test that CSV file content from fixture is readable and contains sample data.

    Args:
        valid_csv_file (str): Path to the mock CSV file.
    """
    with open(valid_csv_file) as f:
        content = f.read()
    assert "Apple" in content
    assert "Phone" in content
    assert "Book Title" in content
