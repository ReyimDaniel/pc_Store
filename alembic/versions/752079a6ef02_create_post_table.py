"""Create post table

Revision ID: 752079a6ef02
Revises: 90eda738b4f0
Create Date: 2025-03-13 00:53:43.255597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '752079a6ef02'
down_revision: Union[str, None] = '90eda738b4f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('body', sa.Text(), server_default='', nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
