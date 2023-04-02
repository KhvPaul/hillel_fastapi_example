"""orders table

Revision ID: 243b47ee2eb8
Revises: a349ec0e039b
Create Date: 2023-04-02 16:43:17.419740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243b47ee2eb8'
down_revision = 'a349ec0e039b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("customer_sub", sa.String(length=48), nullable=False),
        sa.Column("total_price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(["customer_sub"], ["customers.user_sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
    )


def downgrade() -> None:
    op.drop_table("orders")

