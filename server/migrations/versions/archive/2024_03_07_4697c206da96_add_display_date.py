"""Add display_date

Revision ID: 4697c206da96
Revises: fe0bbac910a2
Create Date: 2024-03-07 21:57:49.200754

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "4697c206da96"
down_revision: Union[str, None] = "fe0bbac910a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "document_translations", sa.Column("display_date", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("document_translations", "display_date")
