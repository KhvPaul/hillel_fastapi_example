"""categories table

Revision ID: be5a0f222a4b
Revises: 9ed1270818ee
Create Date: 2023-04-01 15:25:40.882615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be5a0f222a4b'
down_revision = '9ed1270818ee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),

        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("categories")
