from typing import List
from pydantic import ValidationError
from .models import Product
from .utils import log_validation_error
import csv

class Inventory:
    """
    Manages a collection of Product instances.
    
    Methods:
        load_from_csv: Loads and validates products from a CSV file.
        generate_low_stock_report: Writes a report for products below a stock threshold.
    """

    def __init__(self) -> None:
        """Initializes an empty inventory list."""
        self.products: List[Product] = []

    def load_from_csv(self, file_path: str) -> None:
        """
        Loads products from a CSV file and validates each row.

        Args:
            file_path (str): Path to the CSV file.
        """
        with open(file_path, newline="") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # header is line 1
                try:
                    product = Product(**row)
                    self.products.append(product)
                except ValidationError as e:
                    log_validation_error(row_num, e)

    def generate_low_stock_report(self, threshold: int = 10) -> None:
        """
        Generates a text report of products with quantity below the threshold.

        Args:
            threshold (int): Stock quantity threshold.
        """
        with open("low_stock_report.txt", "w") as f:
            for product in self.products:
                if product.quantity < threshold:
                    f.write(f"{product.product_name}: {product.quantity}\n")
