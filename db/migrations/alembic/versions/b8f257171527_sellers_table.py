"""sellers table

Revision ID: b8f257171527
Revises: a90f8e5678b9
Create Date: 2023-04-02 16:31:30.628273

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = 'b8f257171527'
down_revision = 'a90f8e5678b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    gender_enum = ENUM("Male", "Female", "Other", name="genders", create_type=False)

    op.create_table(
        "sellers",
        sa.Column("user_sub", sa.String(length=48), nullable=False),

        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("birthday", sa.DATE(), nullable=False),
        sa.Column("gender", gender_enum, nullable=False),
        sa.Column("phone_number", sa.VARCHAR(length=15), nullable=False),

        sa.ForeignKeyConstraint(["user_sub"], ["users.sub"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_sub"),
        sa.UniqueConstraint("user_sub"),
    )


def downgrade() -> None:
    op.drop_table("sellers")
