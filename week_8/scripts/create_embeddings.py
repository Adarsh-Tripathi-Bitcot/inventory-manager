"""Script: read products and create embeddings into product_embeddings table.

Usage:
    # from repo root (week_8)
    export OPENAI_API_KEY="sk-..."
    export DATABASE_URL="postgresql://user:pass@localhost:5432/inventory"
    python -m scripts.create_embeddings
"""

from __future__ import annotations
import csv
import os
from typing import List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from api.app import create_app
from api.db import db
from api.models import Product, ProductEmbedding
from api.utils.embeddings import embed_texts, OPENAI_EMBEDDING_MODEL

BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "32"))
CSV_PATH = os.path.join(os.getcwd(), "data", "products.csv")


def _row_to_content(row: dict) -> str:
    """Construct a textual context for embedding from a product row or model."""
    parts = [
        row.get("product_name", ""),
        f"type: {row.get('type','')}",
        f"price: {row.get('price','')}",
        f"quantity: {row.get('quantity','')}",
        row.get("expiry_date") or "",
        (row.get("author") or ""),
    ]
    return " | ".join([p for p in parts if p])


def create_from_csv(app):
    """Create embeddings for CSV rows and insert into DB."""
    if not os.path.exists(CSV_PATH):
        print(f"CSV not found: {CSV_PATH}")
        return

    with app.app_context():
        # Optional: create extension if missing (requires DB privileges)
        try:
            db.session.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            db.session.commit()
        except Exception:
            # ignore permission errors; instruct user to run manually if needed
            db.session.rollback()

        to_insert: List[Tuple[int, str]] = []
        with open(CSV_PATH, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                try:
                    product_id = int(row.get("product_id"))
                except Exception:
                    continue
                content = _row_to_content(row)
                to_insert.append((product_id, content))

        # Batch-embed and write to DB
        texts = [c for (_, c) in to_insert]
        embeddings = embed_texts(texts, batch_size=BATCH_SIZE)
        for (product_id, content), emb in zip(to_insert, embeddings):
            # skip existing
            exists = ProductEmbedding.query.filter_by(product_id=product_id).first()
            if exists:
                continue
            pe = ProductEmbedding(product_id=product_id, content=content, embedding=emb)
            db.session.add(pe)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise


if __name__ == "__main__":
    # create Flask app with same default configs as your other week code
    app = create_app()
    print(f"Using embedding model: {OPENAI_EMBEDDING_MODEL}")
    create_from_csv(app)
    print("Done.")
