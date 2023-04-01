"""drop users and user_profiles table

Revision ID: f45a1978a73f
Revises: 3ad4ef1ad9d0
Create Date: 2023-04-01 14:58:10.530740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f45a1978a73f'
down_revision = '3ad4ef1ad9d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("user_profiles")
    op.execute("DROP TYPE genders;")
    op.drop_table("users")


def downgrade() -> None:
    op.create_table(
        "users",
        sa.Column("sub", sa.String(length=48), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password", sa.Text, nullable=False),

        sa.PrimaryKeyConstraint("sub"),
        sa.UniqueConstraint("sub"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "user_profiles",
        sa.Column("user_sub", sa.String(length=48), nullable=False),
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
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(["user_sub"], ["users.sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_sub"),
        sa.UniqueConstraint("user_sub"),
    )
