"""Create record, edition, collection tables.

Revision ID: 2d29a0aea4db
Revises:
Create Date: 2023-12-29 16:11:43.829579

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2d29a0aea4db'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the record, edition, and collection tables."""
    op.create_table(
        'record',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(200), nullable=False, index=True),
        sa.Column('filename', sa.String(255), nullable=False, index=True),
        sa.Column('record_path', sa.String(1000), nullable=False, index=True),
        sa.Column('checksum', sa.String(100), nullable=False),
        sa.Column('mimetype', sa.String(100), nullable=False),
        sa.Column('size', sa.Integer, nullable=False),
        sa.Column('created', sa.DateTime, nullable=False,
                  server_default=sa.func.now())
    )

    op.create_table(
        'edition',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('native_id', sa.Integer, sa.ForeignKey('record.id'),
                  index=True, nullable=False)
    )

    op.create_table(
        'collection',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False, index=True),
        sa.Column('current_edition_id', sa.Integer,
                  sa.ForeignKey('record.id'), nullable=False, index=True),
    )

    op.create_table(
        'collection_x_edition',
        sa.Column('collection_id', sa.Integer, sa.ForeignKey('collection.id'),
                  primary_key=True, index=True),
        sa.Column('edition_id', sa.Integer, sa.ForeignKey('record.id'),
                  primary_key=True, index=True)
        )


def downgrade() -> None:
    """Drop the record, edition, and collections tables."""
    op.drop_table('collection_x_edition')
    op.drop_table('collection')
    op.drop_table('edition')
    op.drop_table('record')
