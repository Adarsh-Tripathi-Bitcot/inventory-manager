"""Constants used across the Week-8 and Week-9 embedding pipeline."""

# --- OpenAI Config ---
OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
EMBEDDING_DIM: int = 1536
OPENAI_TEMPERATURE: float = 0.3

# --- Hugging Face Config ---
HF_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

# --- Chunking configuration ---
CHUNK_SIZE: int = 300
CHUNK_OVERLAP: int = 50

# --- Vector store collections ---
COLLECTION_NAME: str = "product_embeddings"
HF_COLLECTION_NAME: str = "product_embeddings_hf"


# New for Ollama
OLLAMA_MODEL = "llama3"
OLLAMA_TEMPERATURE = 0.0