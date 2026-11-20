"""stock not null and backfill

Revision ID: d1e2f3a4b5c6
Revises: bf7449f35aee
Create Date: 2026-11-17 23:59:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, Sequence[str], None] = 'bf7449f35aee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Backfill and NOT NULL for products.stock / products.in_stock."""
    # Las filas creadas antes de existir la columna quedaron en NULL.
    op.execute("UPDATE products SET stock = 0 WHERE stock IS NULL")
    op.execute("UPDATE products SET in_stock = true WHERE in_stock IS NULL")

    op.alter_column(
        'products', 'stock',
        existing_type=sa.Integer(),
        nullable=False,
        server_default=sa.text('0'),
    )
    op.alter_column(
        'products', 'in_stock',
        existing_type=sa.Boolean(),
        nullable=False,
    )


def downgrade() -> None:
    """Revierte los NOT NULL y el default."""
    op.alter_column(
        'products', 'in_stock',
        existing_type=sa.Boolean(),
        nullable=True,
    )
    op.alter_column(
        'products', 'stock',
        existing_type=sa.Integer(),
        nullable=True,
        server_default=None,
    )
