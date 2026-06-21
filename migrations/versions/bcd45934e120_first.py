"""first

Revision ID: bcd45934e120
Revises: 
Create Date: 2026-06-19 19:10:26.550155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcd45934e120'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'platform',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('platform')

