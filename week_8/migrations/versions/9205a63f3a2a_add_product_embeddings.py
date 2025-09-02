"""add product_embeddings

Revision ID: 9205a63f3a2a
Revises: c923c71ebb9d
Create Date: 2025-09-01 16:xx:xx
"""
from alembic import op
import sqlalchemy as sa

# Import Vector type helper from pgvector
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "9205a63f3a2a"
down_revision = "c923c71ebb9d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure extension exists (may require privileges)
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create table with raw SQL (vector type used literally)
    op.execute(
        '''
        CREATE TABLE IF NOT EXISTS product_embeddings (
            id serial PRIMARY KEY,
            product_id integer REFERENCES products (product_id) NOT NULL,
            content text NOT NULL,
            embedding vector(1536) NOT NULL
        );
        '''
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_product_embeddings_product_id"), table_name="product_embeddings")
    op.drop_table("product_embeddings")
