from pydantic import BaseModel, Field, ValidationError
import csv
from typing import List

class Product(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0.0)


def load_and_validate_products(filename: str) -> List[Product]:
    products = []
    with open(filename, "r") as f, open("errors.log", "w") as error_log:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # start=2 for header offset
            try:
                product = Product(**row)
                products.append(product)
            except ValidationError as e:
                error_log.write(f"Row {i}: {e.errors()}\n")
    return products


def generate_low_stock_report(products: List[Product], threshold: int = 10):
    with open("low_stock_report.txt", "w") as f:
        f.write("Low Stock Products:\n")
        for product in products:
            if product.quantity < threshold:
                f.write(f"{product.product_name}: {product.quantity}\n")

def main():
    products = load_and_validate_products("inventory.csv")
    generate_low_stock_report(products)

if __name__ == "__main__":
    main()
