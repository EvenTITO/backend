"""reviews, submissions, works

Revision ID: b10182ec29bd
Revises: a85757302459
Create Date: 2024-07-26 01:03:14.366161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b10182ec29bd'
down_revision: Union[str, None] = 'a85757302459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('works',
    sa.Column('id_event', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('track', sa.String(), nullable=False),
    sa.Column('stage', sa.String(), nullable=False),
    sa.Column('deadline_date', sa.Date(), nullable=True),
    sa.Column('id_author', sa.String(), nullable=False),
    sa.Column('id_reviewer', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_author'], ['users.id'], ),
    sa.ForeignKeyConstraint(['id_event'], ['events.id'], ),
    sa.ForeignKeyConstraint(['id_reviewer'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_event', 'id'),
    sa.UniqueConstraint('id_event', 'title', name='event_id_title_uc')
    )
    op.create_table('submissions',
    sa.Column('id_event', sa.String(), nullable=False),
    sa.Column('id_work', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('abstract', sa.String(), nullable=True),
    sa.Column('keywords', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('authors', sa.JSON(), nullable=True),
    sa.Column('review_decision', sa.String(), nullable=True),
    sa.Column('review_comments', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_event', 'id_work'], ['works.id_event', 'works.id'], name='fk_work_from_submission'),
    sa.PrimaryKeyConstraint('id_event', 'id_work', 'id')
    )
    op.create_table('reviews',
    sa.Column('id_event', sa.String(), nullable=False),
    sa.Column('id_work', sa.Integer(), nullable=False),
    sa.Column('id_submission', sa.Integer(), nullable=False),
    sa.Column('id_reviewer', sa.String(), nullable=False),
    sa.Column('review', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['id_event', 'id_work', 'id_submission'], ['submissions.id_event', 'submissions.id_work', 'submissions.id'], name='fk_submission_from_review'),
    sa.ForeignKeyConstraint(['id_reviewer'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_event', 'id_work', 'id_submission', 'id_reviewer')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('submissions')
    op.drop_table('works')
    # ### end Alembic commands ###
