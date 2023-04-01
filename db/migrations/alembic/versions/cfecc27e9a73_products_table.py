"""products table

Revision ID: cfecc27e9a73
Revises: be5a0f222a4b
Create Date: 2023-04-01 15:57:17.058965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfecc27e9a73'
down_revision = 'be5a0f222a4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("available_count", sa.Integer(), nullable=False, server_default="0"),

        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("products")
