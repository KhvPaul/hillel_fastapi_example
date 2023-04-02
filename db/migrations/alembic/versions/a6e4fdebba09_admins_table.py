"""admins table

Revision ID: a6e4fdebba09
Revises: 89d31040252f
Create Date: 2023-04-02 16:21:55.074764

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = 'a6e4fdebba09'
down_revision = '89d31040252f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("sub", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.Text, nullable=False),

        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),

        sa.PrimaryKeyConstraint("sub"),
        sa.UniqueConstraint("sub"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("admins")
