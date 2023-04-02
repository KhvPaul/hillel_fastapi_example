"""customers table

Revision ID: a90f8e5678b9
Revises: a6e4fdebba09
Create Date: 2023-04-02 16:25:20.827038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a90f8e5678b9'
down_revision = 'a6e4fdebba09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customers",
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

        sa.ForeignKeyConstraint(["user_sub"], ["users.sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_sub"),
        sa.UniqueConstraint("user_sub"),
    )


def downgrade() -> None:
    op.drop_table("customers")
    op.execute("DROP TYPE genders;")