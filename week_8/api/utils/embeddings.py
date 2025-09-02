"""OpenAI embedding helpers used by ingestion scripts / RAG pipeline.

This module uses the official OpenAI Python client. It defaults to the
text-embedding-3-small model and provides small, safe batching.
"""

from __future__ import annotations
import os
from typing import List, Iterable
from openai import OpenAI

OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")  # for later RAG steps

def get_openai_client() -> OpenAI:
    """Return a configured OpenAI client; raises if API key missing."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def embed_texts(texts: Iterable[str], batch_size: int = 32) -> List[List[float]]:
    """Create embeddings for a list of texts in batches.

    Args:
        texts: Iterable of strings to embed.
        batch_size: batch size for the embeddings.create calls.

    Returns:
        A list of embeddings (each an array of floats) in the same order as texts.
    """
    client = get_openai_client()
    results: List[List[float]] = []
    batch: List[str] = []
    for text in texts:
        batch.append(text)
        if len(batch) >= batch_size:
            resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=batch)
            results.extend([r.embedding for r in resp.data])
            batch = []
    if batch:
        resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=batch)
        results.extend([r.embedding for r in resp.data])
    return results
