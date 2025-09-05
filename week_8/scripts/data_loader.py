# week_8/scripts/data_loader.py
import logging
import os
from typing import List, Dict
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_products() -> List[Dict]:
    """
    Load product data from the database.
    Returns a list of dictionaries with product_id, product_name, and combined description.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    logger.info("Connecting to database...")
    with psycopg2.connect(db_url, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT product_id, product_name, quantity, price, type,
                       expiry_date, warranty_period, author, pages, created_by
                FROM products
            """)
            rows = cursor.fetchall()

            products = []
            for row in rows:
                description_parts = [
                    f"Type: {row['type']}" if row.get("type") else "",
                    f"Price: {row['price']}" if row.get("price") else "",
                    f"Quantity: {row['quantity']}" if row.get("quantity") else "",
                    f"Expiry Date: {row['expiry_date']}" if row.get("expiry_date") else "",
                    f"Warranty Period: {row['warranty_period']}" if row.get("warranty_period") else "",
                    f"Author: {row['author']}" if row.get("author") else "",
                    f"Pages: {row['pages']}" if row.get("pages") else "",
                    f"Created By: {row['created_by']}" if row.get("created_by") else "",
                ]
                description = " | ".join([part for part in description_parts if part])

                products.append(
                    {
                        "product_id": row["product_id"],
                        "product_name": row["product_name"],
                        "description": description,
                    }
                )

            logger.info(f"Loaded {len(products)} products from database.")
            return products
