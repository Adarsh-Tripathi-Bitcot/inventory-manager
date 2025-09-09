from typing import List

# Load model once
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def embed_texts_hf(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using Hugging Face SentenceTransformer.
    """
    return MODEL_NAME.encode(texts, convert_to_numpy=True).tolist()
