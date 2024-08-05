"""empty message

Revision ID: 32840600c693
Revises: e3c1ff41ddc4
Create Date: 2024-07-30 10:45:03.062056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32840600c693'
down_revision: Union[str, None] = 'e3c1ff41ddc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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


def downgrade() -> None:
    pass
