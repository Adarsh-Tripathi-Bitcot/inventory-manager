"""Database seeding CLI command for the Inventory API."""

import csv
import os
import click
from typing import Type
from flask.cli import with_appcontext
from pydantic import ValidationError, BaseModel

from .db import db
from .models import Product
from .schemas import (
    ProductBase,
    FoodProductCreate,
    ElectronicProductCreate,
    BookProductCreate,
)

CSV_PATH: str = os.path.join(os.getcwd(), "data", "products.csv")


@click.command("seed-db")
@with_appcontext
def seed_db() -> None:
    """Seed the database with products from CSV."""
    if not os.path.exists(CSV_PATH):
        click.echo(f"CSV file not found at {CSV_PATH}")
        return

    added: int = 0
    skipped: int = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        reader: csv.DictReader[str] = csv.DictReader(fh)
        for row in reader:
            type_value: str = (row.get("type") or row.get("category") or "").strip().lower()
            schema_cls: Type[BaseModel] = {
                "food": FoodProductCreate,
                "electronic": ElectronicProductCreate,
                "book": BookProductCreate,
            }.get(type_value, ProductBase)

            try:
                validated: BaseModel = schema_cls(**row)
            except ValidationError as e:
                with open("errors.log", "a", encoding="utf-8") as ef:
                    ef.write(f"Row {row} validation error: {e}\n")
                skipped += 1
                continue

            if Product.query.filter_by(product_id=validated.product_id).first():
                skipped += 1
                continue

            p: Product = Product(
                product_id=validated.product_id,
                product_name=validated.product_name,
                quantity=validated.quantity,
                price=validated.price,
                type=type_value or None,
                expiry_date=getattr(validated, "expiry_date", None),
                warranty_period=getattr(validated, "warranty_period", None),
                author=getattr(validated, "author", None),
                pages=getattr(validated, "pages", None),
            )
            db.session.add(p)
            added += 1

        db.session.commit()
    click.echo(f"Seeding finished. Added: {added}. Skipped: {skipped}.")
