"""change works models

Revision ID: b495d697c9c6
Revises: b10182ec29bd
Create Date: 2024-07-26 16:49:51.193195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b495d697c9c6'
down_revision: Union[str, None] = 'b10182ec29bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submissions', 'keywords')
    op.drop_column('submissions', 'authors')
    op.drop_column('submissions', 'abstract')
    op.add_column('works', sa.Column('abstract', sa.String(), nullable=True))
    op.add_column('works', sa.Column('keywords', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('works', sa.Column('authors', sa.JSON(), nullable=True))
    op.drop_column('works', 'stage')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('stage', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('works', 'authors')
    op.drop_column('works', 'keywords')
    op.drop_column('works', 'abstract')
    op.add_column('submissions', sa.Column('abstract', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('submissions', sa.Column('authors', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('submissions', sa.Column('keywords', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###