from typing import List
from pydantic import ValidationError
from .models import Product, FoodProduct, ElectronicProduct, BookProduct
from .utils import log_validation_error
import csv


class Inventory:
    """
    Manages a collection of Product instances.

    Methods:
        load_from_csv: Loads and validates products from a CSV file.
        generate_low_stock_report: Writes a report for products below a stock threshold.
        print_summary_dashboard: Prints inventory summary on the terminal.
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
        try:
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):  # header is line 1
                    # Safely convert empty strings to None
                    for key, value in row.items():
                        row[key] = value if (value is not None and value.strip() != "") else None

                    try:
                        product_type = row.get("type")
                        if product_type == "food":
                            product = FoodProduct(**row)
                        elif product_type == "electronic":
                            product = ElectronicProduct(**row)
                        elif product_type == "book":
                            product = BookProduct(**row)
                        else:
                            product = Product(**row)
                        self.products.append(product)
                    except ValidationError as e:
                        log_validation_error(row_num, e)
        except Exception as e:
            print(f"Error loading CSV file {file_path}: {e}")

    def generate_low_stock_report(self, threshold: int = 10) -> None:
        """
        Generates a text report of products with quantity below the threshold.

        Args:
            threshold (int): Stock quantity threshold.
        """
        try:
            with open("low_stock_report.txt", "w") as f:
                for product in self.products:
                    if product.quantity < threshold:
                        f.write(f"{product.product_name}: {product.quantity}\n")
        except Exception as e:
            print(f"Error generating low stock report: {e}")

    def print_summary_dashboard(self) -> None:
        """
        Prints the inventory summary dashboard:
        - Total products count
        - Total quantity of all products
        - Highest sale product (by total value)
        - Total inventory value
        """
        try:
            total_products = len(self.products)
            total_quantity = sum(product.quantity for product in self.products)
            total_value = sum(product.get_total_value() for product in self.products)

            # Get product with highest total sale value
            highest_sale_product = max(self.products, key=lambda p: p.get_total_value(), default=None)

            print("\nINVENTORY SUMMARY DASHBOARD\n")
            print(f"TOTAL PRODUCTS  : {total_products}")
            print(f"TOTAL QUANTITY  : {total_quantity}")
            if highest_sale_product:
                print(
                    f"HIGHEST SALE PRODUCT : "
                    f"{highest_sale_product.product_name} (Rs {highest_sale_product.get_total_value():,.2f})"
                )
            else:
                print("HIGHEST SALE PRODUCT : N/A")
            print(f"Total inventory value : Rs {total_value:,.2f}\n")
        except Exception as e:
            print(f"Error printing summary dashboard: {e}")
