"""categories table

Revision ID: 16c165e46ca2
Revises: 84561d6a015b
Create Date: 2023-04-02 16:38:35.769136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c165e46ca2'
down_revision = '84561d6a015b'
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
