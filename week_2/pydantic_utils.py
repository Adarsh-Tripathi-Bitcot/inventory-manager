# Define a BaseModel
import csv
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Literal  # noqa: F401


class Item(BaseModel):
    name: str
    quantity: int = Field(gt=0)  # Must be > 0
    price: float

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty.")
        return v


# Use It to Validate CSV Rows
with open("items.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            item = Item(**row)
            print(f"{item.name} -> {item.quantity} @ ₹{item.price}")
        except ValidationError as e:
            print("Invalid row:", row)
            print(e)
