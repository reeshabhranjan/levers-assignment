"""Initial migration

Revision ID: 45bb3ee82776
Revises: 
Create Date: 2024-04-15 05:04:58.128863

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '45bb3ee82776'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bills',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_bills_id'), 'bills', ['id'], unique=False)
    op.create_table('sub_bills',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
                    sa.Column('reference', sa.String(), nullable=True),
                    sa.Column('bill_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['bill_id'], ['bills.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('reference')
                    )
    op.create_index(op.f('ix_sub_bills_id'), 'sub_bills', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sub_bills_id'), table_name='sub_bills')
    op.drop_table('sub_bills')
    op.drop_index(op.f('ix_bills_id'), table_name='bills')
    op.drop_table('bills')
    # ### end Alembic commands ###