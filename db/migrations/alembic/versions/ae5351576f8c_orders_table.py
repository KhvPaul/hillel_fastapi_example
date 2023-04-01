"""orders table

Revision ID: ae5351576f8c
Revises: a475e4246e90
Create Date: 2023-04-01 16:46:28.791352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae5351576f8c'
down_revision = 'a475e4246e90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("customer_sub", sa.String(length=48), nullable=False),
        sa.Column("total_price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(["customer_sub"], ["customers.sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
    )


def downgrade() -> None:
    op.drop_table("orders")
