"""Add messages model

Revision ID: 61139fc047c9
Revises: 4643236904f7
Create Date: 2024-07-26 17:51:28.046017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61139fc047c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer, autoincrement=True, unique=True, primary_key=True),
        sa.Column('user1', sa.String, unique=True),
        sa.Column('user2', sa.String, unique=True),
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, autoincrement=True, unique=True, primary_key=True),
        sa.Column('chat', sa.Integer, unique=True),
        sa.Column('user', sa.String, unique=True),
        sa.Column('text', sa.String),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
