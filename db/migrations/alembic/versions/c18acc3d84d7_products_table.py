"""products table

Revision ID: c18acc3d84d7
Revises: 16c165e46ca2
Create Date: 2023-04-02 16:39:30.007593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c18acc3d84d7'
down_revision = '16c165e46ca2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("available_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("manufacturer_pk", sa.String(length=48), nullable=False),
        sa.Column("seller_sub", sa.String(length=48), nullable=False),

        sa.ForeignKeyConstraint(["manufacturer_pk"], ["manufacturers.pk"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["seller_sub"], ["sellers.user_sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("products")
