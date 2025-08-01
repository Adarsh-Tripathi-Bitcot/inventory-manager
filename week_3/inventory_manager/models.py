from pydantic import BaseModel, Field
from datetime import date


class Product(BaseModel):
    """
    Represents a generic product.

    Attributes:
        product_id (str): Unique identifier.
        product_name (str): Name of the product.
        quantity (int): Quantity in stock (must be non-negative).
        price (float): Price per unit (must be positive).
    """

    product_id: str
    product_name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0.0)

    def get_total_value(self) -> float:
        """
        Calculates the total stock value.

        Returns:
            float: quantity * price
        """
        return self.quantity * self.price


class FoodProduct(Product):
    """
    A specialized product with an expiry date.

    Attributes:
        expiry_date (date): Expiry date of the food product.
    """

    expiry_date: date


class ElectronicProduct(Product):
    """
    A specialized product with a warranty period.

    Attributes:
        warranty_period (int): Warranty in months.
    """

    warranty_period: int


class BookProduct(Product):
    """
    A specialized product with an author.

    Attributes:
        author (str): Author of the book.
    """

    author: str
