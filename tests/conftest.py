import pytest
from datetime import date
from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct


@pytest.fixture
def base_product() -> Product:
    """Returns a generic base Product.

    Returns:
        Product: A basic product instance.
    """
    return Product(
        product_id="P001",
        product_name="Generic Product",
        quantity=10,
        price=20.0
    )


@pytest.fixture
def food_product() -> FoodProduct:
    """Returns a FoodProduct with a future expiry date.

    Returns:
        FoodProduct: A valid food product.
    """
    return FoodProduct(
        product_id="F001",
        product_name="Bread",
        quantity=5,
        price=2.5,
        expiry_date=date(2025, 12, 31)
    )


@pytest.fixture
def electronic_product() -> ElectronicProduct:
    """Returns an ElectronicProduct with a warranty period.

    Returns:
        ElectronicProduct: A valid electronic product.
    """
    return ElectronicProduct(
        product_id="E001",
        product_name="Smartphone",
        quantity=3,
        price=299.99,
        warranty_period=24
    )


@pytest.fixture
def book_product() -> BookProduct:
    """Returns a BookProduct with author and page count.

    Returns:
        BookProduct: A valid book product.
    """
    return BookProduct(
        product_id="B001",
        product_name="Python 101",
        quantity=7,
        price=15.0,
        author="John Doe",
        pages=300
    )


@pytest.fixture
def valid_csv_file(tmp_path) -> str:
    """Creates a temporary CSV file with valid product data.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        str: Path to the generated CSV file.
    """
    csv_data = """product_id,product_name,quantity,price,category,expiry_date,warranty_years,author,genre
        F1,Apple,10,1.2,food,2025-12-31,,, 
        E1,Phone,5,299.99,electronic,,2,, 
        B1,Book Title,3,9.99,book,,,John Doe,Fiction
    """
    file_path = tmp_path / "products.csv"
    file_path.write_text(csv_data)
    return str(file_path)
