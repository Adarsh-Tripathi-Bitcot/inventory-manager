"""Database seeding CLI command for the Inventory API."""

import csv
import os
import click
from flask.cli import with_appcontext
from pydantic import ValidationError

from .db import db
from .models import Product
from .schemas import (
    ProductBase,
    FoodProductCreate,
    ElectronicProductCreate,
    BookProductCreate,
)

CSV_PATH = os.path.join(os.getcwd(), "data", "products.csv")


@click.command("seed-db")
@with_appcontext
def seed_db() -> None:
    """Seed the database with products from CSV.

    Reads `data/products.csv`, validates rows using Pydantic schemas,
    and inserts them into the database if not already present.

    Logs validation errors to `errors.log`.

    Returns:
        None
    """
    if not os.path.exists(CSV_PATH):
        click.echo(f"CSV file not found at {CSV_PATH}")
        return

    added = 0
    skipped = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            type_value = (row.get("type") or row.get("category") or "").strip().lower()
            schema_cls = {
                "food": FoodProductCreate,
                "electronic": ElectronicProductCreate,
                "book": BookProductCreate,
            }.get(type_value, ProductBase)

            try:
                validated = schema_cls(**row)
            except ValidationError as e:
                with open("errors.log", "a", encoding="utf-8") as ef:
                    ef.write(f"Row {row} validation error: {e}\n")
                skipped += 1
                continue

            if Product.query.filter_by(product_id=validated.product_id).first():
                skipped += 1
                continue

            p = Product(
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
