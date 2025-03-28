"""Create profile table

Revision ID: c6fa23aa57f5
Revises: 752079a6ef02
Create Date: 2025-03-22 01:02:56.518459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6fa23aa57f5'
down_revision: Union[str, None] = '752079a6ef02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###
