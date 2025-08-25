"""Remove id column, set product_id as primary key

Revision ID: 59da043a30bd
Revises: 28c0bb1ce72a
Create Date: 2025-08-20 17:40:34.520559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59da043a30bd'
down_revision = '28c0bb1ce72a'
branch_labels = None
depends_on = None


def upgrade():
    # Drop id column first
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('id')

    # Alter product_id from varchar → integer with explicit cast
    op.execute('ALTER TABLE products ALTER COLUMN product_id TYPE INTEGER USING product_id::integer')

    # Make product_id the primary key
    op.create_primary_key("pk_products", "products", ["product_id"])


def downgrade():
    # Reverse changes if you downgrade
    op.drop_constraint("pk_products", "products", type_="primary")
    op.alter_column("products", "product_id",
                    existing_type=sa.Integer(),
                    type_=sa.VARCHAR(length=64))
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.create_primary_key("pk_products", ["id"])