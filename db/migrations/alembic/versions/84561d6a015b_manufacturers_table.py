"""manufacturers table

Revision ID: 84561d6a015b
Revises: b8f257171527
Create Date: 2023-04-02 16:37:28.472350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84561d6a015b'
down_revision = 'b8f257171527'
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
