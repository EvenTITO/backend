"""add payments and review tables

Revision ID: cf840803ab9f
Revises: 
Create Date: 2024-09-14 15:40:25.616171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf840803ab9f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('event_id', sa.UUID(), nullable=False),
    sa.Column('inscription_id', sa.UUID(), nullable=False),
    sa.Column('fare_name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('works', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_update', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_payment_event_id', 'payments', ['event_id'], unique=False)
    op.create_index('ix_payment_inscription_id', 'payments', ['inscription_id'], unique=False)
    op.create_table('reviews',
    sa.Column('submission_id', sa.UUID(), nullable=True),
    sa.Column('reviewer_id', sa.String(length=128), nullable=True),
    sa.Column('event_id', sa.UUID(), nullable=True),
    sa.Column('work_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('review', sa.JSON(), nullable=True),
    sa.Column('shared', sa.Boolean(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_update', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ),
    sa.ForeignKeyConstraint(['work_id'], ['works.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('submissions', sa.Column('state', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submissions', 'state')
    op.drop_table('reviews')
    op.drop_index('ix_payment_inscription_id', table_name='payments')
    op.drop_index('ix_payment_event_id', table_name='payments')
    op.drop_table('payments')
    # ### end Alembic commands ###
