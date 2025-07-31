from pydantic import BaseModel, Field


class Product(BaseModel):
    """Represents a generic product with basic attributes."""

    product_id: str
    product_name: str
    quantity: int = Field(ge=0)
    price: float = Field(gt=0.0)

    def get_total_value(self) -> float:
        """
        Calculate the total value of the product's inventory.

        Returns:
            float: Total value (price * quantity).
        """
        return self.quantity * self.price