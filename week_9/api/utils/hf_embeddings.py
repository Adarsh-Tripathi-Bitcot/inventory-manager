"""Hugging Face embedding helpers used by ingestion scripts / RAG pipeline."""

from __future__ import annotations
from typing import List, Iterable
from sentence_transformers import SentenceTransformer
from week_9.api.constants import HF_EMBEDDING_MODEL

# Load Hugging Face model once
_model = SentenceTransformer(HF_EMBEDDING_MODEL)


def embed_texts_hf(texts: Iterable[str], batch_size: int = 32) -> List[List[float]]:
    """
    Create embeddings for a list of texts in batches using Hugging Face model.

    Args:
        texts (Iterable[str]): Input texts.
        batch_size (int): Batch size for encoding.

    Returns:
        List[List[float]]: Embedding vectors.
    """
    results: List[List[float]] = []
    batch: List[str] = []

    for text in texts:
        batch.append(text)
        if len(batch) >= batch_size:
            results.extend(_model.encode(batch, convert_to_numpy=True).tolist())
            batch = []

    if batch:
        results.extend(_model.encode(batch, convert_to_numpy=True).tolist())

    return results


class HFEmbeddingWrapper:
    """Adapter to make Hugging Face embeddings compatible with LangChain PGVector."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return embed_texts_hf(texts)

    def embed_query(self, text: str) -> List[float]:
        return embed_texts_hf([text])[0]
