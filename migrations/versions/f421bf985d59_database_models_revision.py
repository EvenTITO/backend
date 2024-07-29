"""database models revision

Revision ID: f421bf985d59
Revises: b495d697c9c6
Create Date: 2024-07-27 15:30:27.924167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f421bf985d59'
down_revision: Union[str, None] = 'b495d697c9c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('works', 'abstract',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('works', 'keywords',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.alter_column('works', 'authors',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('works', 'deadline_date',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('works', 'deadline_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('works', 'authors',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('works', 'keywords',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('works', 'abstract',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###