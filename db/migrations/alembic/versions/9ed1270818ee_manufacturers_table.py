"""manufacturers table

Revision ID: 9ed1270818ee
Revises: 0934d2f9f564
Create Date: 2023-04-01 15:18:43.215027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed1270818ee'
down_revision = '0934d2f9f564'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "manufacturers",
        sa.Column("pk", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.VARCHAR(length=15), nullable=False),
        sa.Column("mailing_address", sa.VARCHAR(length=1023), nullable=False),

        sa.PrimaryKeyConstraint("pk"),
        sa.UniqueConstraint("pk"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("manufacturers")
