"""sellers table

Revision ID: d8eca73c6b27
Revises: a76d9fe85d82
Create Date: 2023-04-01 15:02:58.533179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8eca73c6b27'
down_revision = 'a76d9fe85d82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sellers",
        sa.Column("sub", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.Text, nullable=False),

        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),

        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("birthday", sa.DATE(), nullable=False),
        sa.Column(
            "gender",
            sa.Enum(
                "Male",
                "Female",
                "Other",
                name="genders",
            ),
            nullable=False
        ),
        sa.Column("phone_number", sa.VARCHAR(length=15), nullable=False),

        sa.PrimaryKeyConstraint("sub"),
        sa.UniqueConstraint("sub"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("sellers")
