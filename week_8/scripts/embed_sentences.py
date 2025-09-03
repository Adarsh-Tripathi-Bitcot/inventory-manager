#!/usr/bin/env python3
"""
Script: Generate embeddings for sentences and store in sentence_embeddings table.

Usage:
  # Run from week_8 folder
  export OPENAI_API_KEY="sk-..."
  python -m scripts.embed_sentences
"""

from __future__ import annotations
import os
from typing import List
from api.app import create_app
from api.db import db
from api.models import SentenceEmbedding
from api.utils.embeddings import embed_texts

# Batch size for embeddings
BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "32"))

# Sentences to embed
SENTENCES: List[str] = [
    "The product inventory management system tracks all items.",
    "We store products, quantities, prices, and other metadata.",
    "Embedding vectors allow semantic search across product descriptions.",
    "Flask + SQLAlchemy manages the database interactions cleanly.",
]

def run_embeddings(sentences: List[str], batch_size: int = BATCH_SIZE):
    """Embed sentences and insert into the database."""
    app = create_app()
    with app.app_context():  # ✅ Use Flask app context
        # Optional: create vector extension if missing
        try:
            db.session.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            db.session.commit()
        except Exception:
            db.session.rollback()

        # Generate embeddings
        embeddings = embed_texts(sentences, batch_size=batch_size)

        # Insert into DB
        inserted_count = 0
        for content, emb in zip(sentences, embeddings):
            exists = SentenceEmbedding.query.filter_by(content=content).first()
            if exists:
                continue
            se = SentenceEmbedding(content=content, embedding=emb)
            db.session.add(se)
            inserted_count += 1

        db.session.commit()
        print(f"Inserted {inserted_count} new embeddings into sentence_embeddings table.")

if __name__ == "__main__":
    run_embeddings(SENTENCES)
