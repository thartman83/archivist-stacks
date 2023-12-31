"""Add edition_number

Revision ID: 8d139ecad608
Revises: 2d29a0aea4db
Create Date: 2023-12-31 15:35:38.725414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d139ecad608'
down_revision: Union[str, None] = '2d29a0aea4db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the edition_number as a new indexed column to edition."""
    op.add_column('edition', sa.Column('edition_number', sa.Integer,
                                       index=True))
    op.execute("UPDATE edition SET edition_number = 0;")
    op.alter_column('edition', 'edition_number', nullable=False)

    op.rename_table('collection_x_edition', 'collection_edition_assoc')


def downgrade() -> None:
    """Remove the new column."""
    op.drop_column('edition', 'edition_number')
    op.rename_table('collection_edition_assoc', 'collection_x_edition')
