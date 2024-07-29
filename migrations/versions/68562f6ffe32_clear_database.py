"""clear database

Revision ID: 68562f6ffe32
Revises: f9a7e3c00b42
Create Date: 2024-07-29 01:56:16.209337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68562f6ffe32'
down_revision: Union[str, None] = 'f9a7e3c00b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text('DELETE FROM reviews'))
    op.execute(sa.text('DELETE FROM events'))

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('review_status', sa.String(), nullable=False))
    op.add_column('submissions', sa.Column('public_review', sa.Boolean(), nullable=False))
    op.add_column('works', sa.Column('state', sa.String(), nullable=False))
    op.alter_column('works', 'deadline_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.drop_constraint('works_id_reviewer_fkey', 'works', type_='foreignkey')
    op.drop_column('works', 'id_reviewer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('id_reviewer', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('works_id_reviewer_fkey', 'works', 'users', ['id_reviewer'], ['id'])
    op.alter_column('works', 'deadline_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
    op.drop_column('works', 'state')
    op.drop_column('submissions', 'public_review')
    op.drop_column('reviews', 'review_status')
    # ### end Alembic commands ###
