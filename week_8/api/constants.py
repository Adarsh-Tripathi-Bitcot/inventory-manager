# week_8/api/constants.py

"""Constants used across the Week-8 embedding pipeline."""

# Embedding model
OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

# Chat model (will be used later for RAG)
OPENAI_CHAT_MODEL: str = "gpt-4o-mini"

# Embedding dimension for text-embedding-3-small
EMBEDDING_DIM: int = 1536
