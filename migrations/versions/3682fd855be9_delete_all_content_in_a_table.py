"""delete all content in a table

Revision ID: 3682fd855be9
Revises: ef28569649cf
Create Date: 2024-07-27 19:53:16.959730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3682fd855be9'
down_revision: Union[str, None] = 'ef28569649cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text('DELETE FROM organizers'))
    op.execute(sa.text('DELETE FROM events'))



def downgrade() -> None:
    pass
