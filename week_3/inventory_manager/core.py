# week_3/inventory_manager/core.py

import csv
from pathlib import Path
from typing import List, Union
from .models import Product, FoodProduct, ElectronicProduct, BookProduct
from .utils import log_validation_error
from pydantic import ValidationError


class Inventory:
    """Class representing an inventory of products."""

    def __init__(self) -> None:
        """Initialize an empty inventory."""
        self.products: List[Product] = []

    def load_from_csv(self, file_path: Union[str, Path]) -> None:
        """
        Load product data from a CSV file and populate the inventory.

        Args:
            file_path (Union[str, Path]): Path to the CSV file.

        Raises:
            ValueError: If a product category is unrecognized.
            ValidationError: If product data fails validation.
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        category = row.get("category", "").lower()
                        if category == "food":
                            product = FoodProduct(**row)
                        elif category == "electronic":
                            product = ElectronicProduct(**row)
                        elif category == "book":
                            product = BookProduct(**row)
                        else:
                            raise ValueError(f"Unknown category '{category}' in row: {row}")
                        self.products.append(product)
                    except (ValidationError, ValueError) as e:
                        log_validation_error(row, e)
        except Exception as e:
            print(f"Failed to load products from CSV: {e}")

    def generate_low_stock_report(self, report_file: Union[str, Path], threshold: int = 5) -> None:
        """
        Generate a low stock report based on a quantity threshold.

        Args:
            report_file (Union[str, Path]): Path to save the report file.
            threshold (int, optional): Quantity threshold to consider a product as low stock. Defaults to 5.

        Raises:
            Exception: If file writing fails.
        """
        try:
            low_stock = [p for p in self.products if p.quantity < threshold]
            with open(str(report_file), mode="w", encoding="utf-8") as f:
                if not low_stock:
                    f.write("All products are sufficiently stocked.\n")
                else:
                    for p in low_stock:
                        f.write(f"{p.product_name} (ID: {p.product_id}) - Qty: {p.quantity}\n")
        except Exception as e:
            print(f"Error generating low stock report: {e}")

    def print_summary_dashboard(self) -> None:
        """
        Print a summary dashboard showing total products, total quantity,
        highest sale product, and total inventory value.
        """
        total_products = len(self.products)
        total_quantity = sum(p.quantity for p in self.products)
        highest_sale = max(self.products, key=lambda p: p.price * p.quantity, default=None)

        print("Inventory Summary Dashboard")
        print(f"Total Products : {total_products}")
        print(f"Total Quantity : {total_quantity}")

        if highest_sale:
            print(
                f"Highest Sale Product : {highest_sale.product_name} "
                f"(Rs {highest_sale.price * highest_sale.quantity:.2f})"
            )
        else:
            print("Highest Sale Product : N/A")

        total_value = sum(p.price * p.quantity for p in self.products)
        print(f"Total inventory value : Rs {total_value:.2f}")
