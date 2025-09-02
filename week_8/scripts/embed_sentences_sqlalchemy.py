#!/usr/bin/env python3
"""Embed sentences and store into generic_embeddings table using Flask/SQLAlchemy app context.

Usage:
  python -m scripts.embed_sentences_sqlalchemy --sentences "hello world" "another sentence"
  python -m scripts.embed_sentences_sqlalchemy --file data/my_sentences.txt
"""

from __future__ import annotations
import argparse
import os
from typing import List

from sqlalchemy import text
from api.app import create_app
from api.db import db

# Try to use your existing helper; fallback will be handled below.
try:
    from api.utils.embeddings import embed_texts, OPENAI_EMBEDDING_MODEL  
    HAS_EMBED_HELPER = True
except Exception:
    HAS_EMBED_HELPER = False

# Fallback: local small wrapper if embed_texts is absent
def _fallback_embed_texts(texts: List[str], model: str, batch_size: int = 32) -> List[List[float]]:
    """Fallback embedding caller using OpenAI client (works with openai or `openai` package)."""
    try:
        # New OpenAI client
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.embeddings.create(model=model, input=texts)
        return [d.embedding for d in resp.data]
    except Exception:
        import openai  # type: ignore
        openai.api_key = os.getenv("OPENAI_API_KEY")
        resp = openai.Embedding.create(model=model, input=texts)
        return [d["embedding"] for d in resp["data"]]


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def ensure_table_and_extension():
    """Create vector extension (if allowed) and the generic_embeddings table."""
    # extension
    db.session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    db.session.commit()

    # create table
    create_sql = """
    CREATE TABLE IF NOT EXISTS generic_embeddings (
        id serial PRIMARY KEY,
        content text NOT NULL,
        embedding vector(1536) NOT NULL
    );
    """
    db.session.execute(text(create_sql))
    db.session.commit()


def run(sentences: List[str], model: str = DEFAULT_MODEL, batch_size: int = 32):
    with app.app_context():
        ensure_table_and_extension()

        # choose embed function
        if HAS_EMBED_HELPER:
            embeddings = embed_texts(sentences, batch_size=batch_size)
        else:
            embeddings = _fallback_embed_texts(sentences, model=model, batch_size=batch_size)

        # Insert rows
        insert_sql = text("INSERT INTO generic_embeddings (content, embedding) VALUES (:content, :embedding) RETURNING id;")

        inserted = []
        for content, emb in zip(sentences, embeddings):
            # emb should be a python list of floats; SQLAlchemy/psycopg2 + registered pgvector should accept it
            r = db.session.execute(insert_sql, {"content": content, "embedding": emb})
            row_id = r.fetchone()[0]
            inserted.append(row_id)
        db.session.commit()

        # verification
        print(f"Inserted {len(inserted)} rows. Example rows:")
        rows = db.session.execute(text("SELECT id, LEFT(embedding::text, 120) FROM generic_embeddings ORDER BY id DESC LIMIT 5;"))
        for r in rows:
            print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sentences", nargs="+", help="Sentences to embed.")
    group.add_argument("--file", help="File with one sentence per line.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Embedding model name.")
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("EMBED_BATCH_SIZE", "32")))
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            sentences = [line.strip() for line in fh if line.strip()]
    else:
        sentences = args.sentences

    # create Flask app, attach DB
    app = create_app()
    db.init_app(app)

    run(sentences, model=args.model, batch_size=args.batch_size)
