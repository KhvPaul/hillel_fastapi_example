"""add user_role to users table

Revision ID: 3ad4ef1ad9d0
Revises: 03e438c64e06
Create Date: 2023-03-26 20:28:29.267144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad4ef1ad9d0'
down_revision = '03e438c64e06'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE TYPE userroles AS ENUM ('Seller', 'Customer');")
    op.add_column("users", sa.Column(
            "user_role",
            sa.Enum(
                "Seller",
                "Customer",
                name="userroles",
            ),
            nullable=False
        ))


def downgrade():
    op.drop_column("users", "user_role")
    op.execute("DROP TYPE userroles;")
