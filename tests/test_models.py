import pytest
from pydantic import ValidationError
from datetime import date
from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct


@pytest.mark.parametrize(
    "product_id, product_name, quantity, price",
    [
        ("P001", "Item 1", 10, 5.0),
        ("P002", "Item 2", 0, 99.99),
    ],
)
def test_product_valid(product_id: str, product_name: str, quantity: int, price: float) -> None:
    """
    Test Product creation with valid inputs.

    Args:
        product_id (str): Product ID.
        product_name (str): Product name.
        quantity (int): Quantity of the product (>= 0).
        price (float): Price of the product (> 0.0).
    """
    product = Product(
        product_id=product_id,
        product_name=product_name,
        quantity=quantity,
        price=price,
    )
    assert product.product_id == product_id
    assert product.product_name == product_name
    assert product.quantity == quantity
    assert product.price == price


@pytest.mark.parametrize(
    "quantity, price",
    [
        (-1, 10.0),
        (5, -5.0),
        (-3, -9.0),
    ],
)
def test_product_invalid_values(quantity: int, price: float) -> None:
    """
    Test Product model with invalid quantity or price.

    Args:
        quantity (int): Invalid quantity.
        price (float): Invalid price.
    """
    with pytest.raises(ValidationError):
        Product(
            product_id="P999",
            product_name="Invalid",
            quantity=quantity,
            price=price,
        )


def test_food_product_valid() -> None:
    """Test valid FoodProduct creation."""
    food = FoodProduct(
        product_id="F001",
        product_name="Bread",
        quantity=10,
        price=2.5,
        expiry_date=date(2025, 12, 31),
    )
    assert food.expiry_date == date(2025, 12, 31)


def test_food_product_invalid_expiry_date() -> None:
    """Test FoodProduct with missing expiry_date."""
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id="F002",
            product_name="Milk",
            quantity=5,
            price=1.99,
            expiry_date=None,
        )


def test_electronic_product_valid() -> None:
    """Test valid ElectronicProduct creation."""
    elec = ElectronicProduct(
        product_id="E001",
        product_name="Phone",
        quantity=3,
        price=500.0,
        warranty_period=12,
    )
    assert elec.warranty_period == 12


def test_electronic_product_invalid_warranty() -> None:
    """Test ElectronicProduct with missing warranty_period."""
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id="E002",
            product_name="Tablet",
            quantity=1,
            price=350.0,
            warranty_period=None,
        )


def test_book_product_valid() -> None:
    """Test valid BookProduct creation."""
    book = BookProduct(
        product_id="B001",
        product_name="Python 101",
        quantity=7,
        price=15.0,
        author="John Doe",
        pages=300,
    )
    assert book.author == "John Doe"
    assert book.pages == 300


def test_book_product_missing_author() -> None:
    """Test BookProduct with missing author."""
    with pytest.raises(ValidationError):
        BookProduct(
            product_id="B002",
            product_name="C++ Basics",
            quantity=3,
            price=10.0,
            author=None,
            pages=250,
        )


def test_book_product_missing_pages() -> None:
    """Test BookProduct with missing pages."""
    with pytest.raises(ValidationError):
        BookProduct(
            product_id="B003",
            product_name="Go Lang",
            quantity=2,
            price=12.0,
            author="Alex",
            pages=None,
        )
