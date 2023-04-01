"""order_items table

Revision ID: 54a1e4914d49
Revises: ae5351576f8c
Create Date: 2023-04-01 16:52:49.499245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54a1e4914d49'
down_revision = 'ae5351576f8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "order_items",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("order_pk", sa.String(length=48), nullable=False),
        sa.Column("product_pk", sa.String(length=48), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(["order_pk"], ["orders.pk"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_pk"], ["products.pk"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
    )


def downgrade() -> None:
    op.drop_table("order_items")
