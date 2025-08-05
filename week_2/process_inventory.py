from pydantic import BaseModel, Field, ValidationError
import csv
from typing import List


class Product(BaseModel):
    """
    A model representing a single product in inventory.

    Attributes:
        product_id (str): Unique identifier of the product.
        product_name (str): Name of the product.
        quantity (int): Available stock (must be ≥ 0).
        price (float): Price per unit (must be > 0).
    """

    product_id: str
    product_name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0.0)


def load_and_validate_products(filename: str) -> List[Product]:
    """
    Load product data from a CSV file and validate each record using Pydantic.

    Args:
        filename (str): The path to the CSV file containing product data.

    Returns:
        List[Product]: A list of validated Product objects.

    Notes:
        - If a row contains invalid data, the error will be logged to 'errors.log'.
    """
    products: List[Product] = []
    with open(filename, "r") as f, open("errors.log", "w") as error_log:
        reader = csv.DictReader(f)
        for i, row in enumerate(
            reader, start=2
        ):  # start=2 accounts for the header line
            try:
                product = Product(**row)
                products.append(product)
            except ValidationError as e:
                error_log.write(f"Row {i}: {e.errors()}\n")
    return products


def generate_low_stock_report(products: List[Product], threshold: int = 10) -> None:
    """
    Generate a text report for products that are below the stock threshold.

    Args:
        products (List[Product]): The list of validated Product objects.
        threshold (int, optional): The quantity threshold. Defaults to 10.

    Output:
        A file named 'low_stock_report.txt' listing products with stock less than the threshold.
    """
    with open("low_stock_report.txt", "w") as f:
        f.write("Low Stock Products:\n")
        for product in products:
            if product.quantity < threshold:
                f.write(f"{product.product_name}: {product.quantity}\n")


def main() -> None:
    """
    Main function to load and validate products and generate a low stock report.
    """
    products = load_and_validate_products("inventory.csv")
    generate_low_stock_report(products)


if __name__ == "__main__":
    main()
