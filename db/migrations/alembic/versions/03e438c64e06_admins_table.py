"""admins_table

Revision ID: 03e438c64e06
Revises: e766fea769d5
Create Date: 2023-03-26 16:25:38.595688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03e438c64e06'
down_revision = 'e766fea769d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("sub", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.Text, nullable=False),

        sa.PrimaryKeyConstraint("sub"),
        sa.UniqueConstraint("sub"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("admins")
