"""users_table

Revision ID: aa3921a64312
Revises: 
Create Date: 2023-03-25 09:12:35.868651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa3921a64312'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("sub", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.Text, nullable=False),

        sa.PrimaryKeyConstraint("sub"),
        sa.UniqueConstraint("sub"),
    )


def downgrade() -> None:
    op.drop_table("users")
