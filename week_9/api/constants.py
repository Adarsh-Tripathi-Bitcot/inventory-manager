# week_8/api/constants.py

"""Constants used across the Week-8 embedding pipeline."""

# Embedding model
OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

# Chat model (will be used later for RAG)
OPENAI_CHAT_MODEL: str = "gpt-4o-mini"

# Embedding dimension for text-embedding-3-small
EMBEDDING_DIM: int = 1536

# Model temperature
OPENAI_TEMPERATURE: float = 0.3

# Chunking configuration
CHUNK_SIZE: int = 300
CHUNK_OVERLAP: int = 50

# Vector store collection
COLLECTION_NAME = "product_embeddings"