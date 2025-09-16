"""Add llm_cache table for caching

Revision ID: 4a9448b7eb38
Revises: 
Create Date: 2025-09-09 12:43:18.483734
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4a9448b7eb38'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema."""
    # Only apply llm_cache changes, remove langchain_pg_* drops
    with op.batch_alter_table('llm_cache', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiration_time', sa.DateTime(timezone=True), nullable=True))
        batch_op.alter_column('model_name',
                              existing_type=sa.VARCHAR(length=128),
                              type_=sa.String(length=50),
                              existing_nullable=False)
        batch_op.alter_column('created_at',
                              existing_type=postgresql.TIMESTAMP(),
                              type_=sa.DateTime(timezone=True),
                              existing_nullable=True)
        batch_op.drop_constraint(batch_op.f('uix_model_prompt'), type_='unique')
        batch_op.create_unique_constraint(None, ['prompt'])
        batch_op.drop_column('updated_at')


def downgrade():
    """Downgrade database schema."""
    with op.batch_alter_table('llm_cache', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uix_model_prompt'), ['model_name', 'prompt'], postgresql_nulls_not_distinct=False)
        batch_op.alter_column('created_at',
                              existing_type=sa.DateTime(timezone=True),
                              type_=postgresql.TIMESTAMP(),
                              existing_nullable=True)
        batch_op.alter_column('model_name',
                              existing_type=sa.String(length=50),
                              type_=sa.VARCHAR(length=128),
                              existing_nullable=False)
        batch_op.drop_column('expiration_time')
