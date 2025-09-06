"""drop_password_column

Revision ID: 1a2b3c4d5e6f
Revises: 7c8fff0d6f2f
Create Date: 2025-08-25 20:43:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = '7c8fff0d6f2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the legacy plaintext password column if it exists
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('password')


def downgrade() -> None:
    # Recreate the plaintext password column on downgrade
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(), nullable=True))

