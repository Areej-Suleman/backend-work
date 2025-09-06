"""add_cloudinary_columns_to_files

Revision ID: 2b9a7c1d3e4f
Revises: 1a2b3c4d5e6f
Create Date: 2025-08-26 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2b9a7c1d3e4f'
down_revision: Union[str, Sequence[str], None] = '1a2b3c4d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('files') as batch_op:
        batch_op.add_column(sa.Column('public_id', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('storage_type', sa.String(length=50), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('files') as batch_op:
        batch_op.drop_column('storage_type')
        batch_op.drop_column('public_id')

