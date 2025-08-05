from pydantic import BaseModel, Field, model_validator
from datetime import date


class Product(BaseModel):
    """Represents a generic product in the inventory."""

    product_id: str
    product_name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0.0)

    def get_total_value(self) -> float:
        """Returns the total value of this product in stock."""
        return self.quantity * self.price


class FoodProduct(Product):
    """Represents a food product with an expiry date."""

    expiry_date: date

    @model_validator(mode="after")
    def check_expiry_date(self) -> "FoodProduct":
        """Ensures expiry_date is present."""
        if not self.expiry_date:
            raise ValueError("Food products must have an expiry_date")
        return self


class ElectronicProduct(Product):
    """Represents an electronic product with warranty period."""

    warranty_period: int = Field(ge=0)

    @model_validator(mode="after")
    def check_warranty(self) -> "ElectronicProduct":
        """Ensures warranty_period is present."""
        if self.warranty_period is None:
            raise ValueError("Electronic products must have a warranty_period")
        return self


class BookProduct(Product):
    """Represents a book with author and pages."""

    author: str
    pages: int = Field(ge=1)

    @model_validator(mode="after")
    def check_author_and_pages(self) -> "BookProduct":
        """Ensures author and pages are present."""
        if not self.author or self.pages is None:
            raise ValueError("Book products must have both author and pages")
        return self
