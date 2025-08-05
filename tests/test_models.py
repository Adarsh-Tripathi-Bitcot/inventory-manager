import pytest
from pydantic import ValidationError
from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
from datetime import date

# ---------- Base Product Tests ----------

def test_product_total_value():
    product = Product(
        product_id="P001",
        product_name="Keyboard",
        quantity=5,
        price=100.0
    )
    assert product.get_total_value() == 500.0


def test_product_identity_fields():
    product = Product(
        product_id="P004",
        product_name="Webcam",
        quantity=2,
        price=150.0
    )
    assert product.product_id == "P004"
    assert product.product_name == "Webcam"


def test_product_negative_quantity():
    with pytest.raises(ValidationError):
        Product(
            product_id="P002",
            product_name="Mouse",
            quantity=-1,
            price=50.0
        )


def test_product_zero_price():
    with pytest.raises(ValidationError):
        Product(
            product_id="P003",
            product_name="Monitor",
            quantity=5,
            price=0.0
        )


def test_product_zero_quantity():
    product = Product(
        product_id="P005",
        product_name="Pen",
        quantity=0,
        price=10.0
    )
    assert product.get_total_value() == 0.0


def test_product_large_total_value():
    product = Product(
        product_id="P006",
        product_name="Server",
        quantity=1000,
        price=250000.0
    )
    assert product.get_total_value() == 250_000_000.0


def test_product_negative_price():
    with pytest.raises(ValidationError):
        Product(
            product_id="P007",
            product_name="USB Cable",
            quantity=10,
            price=-50.0
        )


def test_product_blank_name():
    product = Product(
        product_id="P008",
        product_name="",
        quantity=1,
        price=10.0
    )
    assert product.product_name == ""  # blank name is allowed, but maybe shouldn't be in real-world


def test_product_id_is_required():
    with pytest.raises(ValidationError):
        Product(
            product_name="Unnamed",
            quantity=1,
            price=100.0
        )

# ---------- FoodProduct Tests ----------

def test_food_product_expiry_field():
    food = FoodProduct(
        product_id="F001",
        product_name="Milk",
        quantity=10,
        price=25.0,
        expiry_date="2025-12-31"
    )
    assert food.expiry_date == date(2025, 12, 31)
    assert food.get_total_value() == 250.0


def test_food_product_missing_expiry():
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id="F002",
            product_name="Yogurt",
            quantity=5,
            price=30.0
        )


def test_food_product_past_expiry_date():
    food = FoodProduct(
        product_id="F003",
        product_name="Old Cheese",
        quantity=1,
        price=20.0,
        expiry_date="2020-01-01"
    )
    assert food.expiry_date == date(2020, 1, 1)  # Validation allows past dates by default

# ---------- ElectronicProduct Tests ----------

def test_electronics_product_warranty_field():
    electronics = ElectronicProduct(
        product_id="E001",
        product_name="Laptop",
        quantity=3,
        price=60000.0,
        warranty_period=2
    )
    assert electronics.warranty_period == 2
    assert electronics.get_total_value() == 180000.0


def test_electronics_product_invalid_warranty():
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id="E002",
            product_name="Headphones",
            quantity=10,
            price=1500.0,
            warranty_period=-1
        )


def test_electronics_product_missing_warranty():
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id="E003",
            product_name="Tablet",
            quantity=2,
            price=15000.0
        )

# ---------- BookProduct Tests ----------

def test_book_product_author_and_pages():
    book = BookProduct(
        product_id="B001",
        product_name="Atomic Habits",
        quantity=8,
        price=499.0,
        author="James Clear",
        pages=320
    )
    assert book.author == "James Clear"
    assert book.pages == 320
    assert book.get_total_value() == 3992.0


def test_book_product_missing_author():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id="B004",
            product_name="Anonymous Book",
            quantity=4,
            price=300.0,
            pages=100
        )


def test_book_product_zero_pages():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id="B003",
            product_name="Zero Page Book",
            quantity=1,
            price=100.0,
            author="Ghost Author",
            pages=0
        )


def test_book_product_blank_author():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id="B005",
            product_name="Unknown",
            quantity=2,
            price=200.0,
            author="",
            pages=150
        )

# ---------- Parametrized Total Value Edge Cases ----------

@pytest.mark.parametrize("quantity,price,expected", [
    (0, 100.0, 0.0),
    (10, 0.01, 0.1),
    (1, 999999.99, 999999.99),
    (999999, 0.01, 9999.99),
    (5, 19.999, 99.995),
])
def test_product_total_value_edge_cases(quantity, price, expected):
    product = Product(
        product_id="PX",
        product_name="EdgeItem",
        quantity=quantity,
        price=price
    )
    assert round(product.get_total_value(), 5) == round(expected, 5)
