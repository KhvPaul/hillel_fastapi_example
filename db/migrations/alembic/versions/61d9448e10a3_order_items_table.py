"""order_items table

Revision ID: 61d9448e10a3
Revises: 243b47ee2eb8
Create Date: 2023-04-02 16:44:02.740408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d9448e10a3'
down_revision = '243b47ee2eb8'
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
