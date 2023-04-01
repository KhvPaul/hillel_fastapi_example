"""update admins table

Revision ID: 0934d2f9f564
Revises: d8eca73c6b27
Create Date: 2023-04-01 15:03:48.754032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0934d2f9f564'
down_revision = 'd8eca73c6b27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("admins", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("admins", sa.Column("updated_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("admins", "created_at")
    op.drop_column("admins", "updated_at")
