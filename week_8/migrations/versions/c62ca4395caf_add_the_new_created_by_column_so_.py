"""Add the new created_by column so manager can only update their own products

Revision ID: c62ca4395caf
Revises: 8e006cceca3e
Create Date: 2025-08-28 17:15:11.184667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c62ca4395caf'
down_revision = '8e006cceca3e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_by", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_products_created_by_users",
            "users",
            ["created_by"],
            ["id"]
        )

    # Populate with a default admin user
    conn = op.get_bind()
    admin_id = conn.execute(sa.text("SELECT id FROM users WHERE role = 'admin' LIMIT 1")).scalar()
    if admin_id:
        conn.execute(sa.text("UPDATE products SET created_by = :admin_id WHERE created_by IS NULL"), {"admin_id": admin_id})


def downgrade():
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_constraint("fk_products_created_by_users", type_="foreignkey")
        batch_op.drop_column("created_by")

