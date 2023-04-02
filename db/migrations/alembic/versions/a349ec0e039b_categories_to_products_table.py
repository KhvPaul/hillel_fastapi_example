"""categories_to_products table

Revision ID: a349ec0e039b
Revises: c18acc3d84d7
Create Date: 2023-04-02 16:42:48.868254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a349ec0e039b'
down_revision = 'c18acc3d84d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories_to_products",
        sa.Column("category_pk", sa.String(length=48), nullable=False),
        sa.Column("product_pk", sa.String(length=48), nullable=False),
        sa.ForeignKeyConstraint(["category_pk"], ["categories.pk"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_pk"], ["products.pk"], ondelete="CASCADE"),
    )
    op.create_unique_constraint(None, "categories_to_products", ["category_pk", "product_pk"])


def downgrade():
    op.drop_table("categories_to_products")
