"""add_chat_name

Revision ID: fbeacd6ad2a5
Revises: 
Create Date: 2024-05-06 02:07:07.218030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbeacd6ad2a5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), server_default='', nullable=False),
    sa.Column('organization_id', sa.UUID(), nullable=True),
    sa.Column('for_system_managers', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('message', sa.String(), server_default='', nullable=False),
    sa.Column('organization_id', sa.UUID(), nullable=True),
    sa.Column('group_id', sa.UUID(), nullable=True),
    sa.Column('wash_id', sa.UUID(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    op.drop_table('chats')
    # ### end Alembic commands ###
