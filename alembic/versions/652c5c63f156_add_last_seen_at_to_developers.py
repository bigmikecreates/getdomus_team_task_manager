"""add last_seen_at to developers

Revision ID: 652c5c63f156
Revises: aaa8f8a8e991
Create Date: 2026-07-22 06:16:21.295903
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652c5c63f156'
down_revision: Union[str, None] = 'aaa8f8a8e991'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('developers', sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('developers', 'last_seen_at')
