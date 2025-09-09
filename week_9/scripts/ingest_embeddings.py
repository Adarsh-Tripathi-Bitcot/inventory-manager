import logging
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
import psycopg2
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..api.utils.hf_embeddings import MODEL_NAME

from week_8.api.constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from week_8.scripts.data_loader import load_products

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


HF_COLLECTION_NAME = "product_embeddings_hf"

def get_already_embedded_product_ids() -> set:
    """
    Fetch product_ids that are already embedded in the langchain_pg_embedding table.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT cmetadata ->> 'product_id' AS product_id
        FROM langchain_pg_embedding
        WHERE cmetadata::jsonb ? 'product_id';
    """)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    embedded_ids = set(int(row[0]) for row in results if row[0] is not None)
    return embedded_ids



def embed_and_store(products: List[Dict]) -> PGVector:
    """
    Generate embeddings for product data and store in pgvector.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info("Initializing OpenAI embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    logger.info("Splitting product data into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    documents: List[Document] = []
    for product in products:
        content = f"{product['product_name']}\n{product.get('description', '')}"
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
        collection_name=HF_COLLECTION_NAME,
    )

    logger.info("Embeddings successfully stored in pgvector.")
    return vector_store


if __name__ == "__main__":
    logger.info("Loading products from database...")
    all_products = load_products()

    logger.info("Checking for already embedded products...")
    embedded_ids = get_already_embedded_product_ids()

    logger.info(f"Found {len(embedded_ids)} products already embedded.")

    new_products = [
        product for product in all_products
        if product["product_id"] not in embedded_ids
    ]

    logger.info(f"Found {len(new_products)} new products to embed.")

    if new_products:
        embed_and_store(new_products)
    else:
        logger.info("No new products to embed.")
