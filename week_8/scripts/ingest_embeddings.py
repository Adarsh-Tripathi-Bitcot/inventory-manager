# week_8/scripts/ingest_embeddings.py
import logging
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

from week_8.api.constants import (
    OPENAI_EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def embed_and_store(products: List[Dict]) -> PGVector:
    """
    Generate embeddings for product data and store in pgvector.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    logger.info("Splitting product data into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    documents: List[Document] = []
    for product in products:
        content = f"{product['product_name']}\n{product['description']}"

        for chunk in text_splitter.split_text(content):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"product_id": product["product_id"]},
                )
            )

    logger.info(f"Generated {len(documents)} chunks for embedding.")

    vector_store = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_string=db_url,
        collection_name="product_embeddings",
    )

    logger.info("Embeddings successfully stored in pgvector.")
    return vector_store


if __name__ == "__main__":
    from week_8.scripts.data_loader import load_products

    logger.info("Loading products to embed...")
    products = load_products()
    embed_and_store(products)
