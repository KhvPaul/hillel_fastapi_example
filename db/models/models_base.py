import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

from pydentic_models import enums

Base = declarative_base()

_uuid = lambda: uuid.uuid4().hex  # noqa future workpiece for function
generate_uuid = lambda: _uuid()  # noqa


class AbstractUser(Base):
    """
    Abstract class that can't be initialized. Used to provide default User attrs (sub, email, password, etc.)
    """

    __abstract__ = True

    sub = sa.Column(
        "sub",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    email = sa.Column("email", sa.String(320), unique=True, nullable=False)
    password = sa.Column("password", sa.Text, nullable=False)

    user_role = sa.Column("user_role", sa.Enum(enums.UserRoles), nullable=False)

    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        "updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class AbstractUserProfile(Base):
    """
    Abstract class that can't be initialized. Used to provide default UserProfile attrs (first_name, last_name, etc)
    """

    __abstract__ = True

    user_sub = sa.Column(
        "user_sub",
        sa.ForeignKey("users.sub", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        primary_key=True,
    )

    first_name = sa.Column("first_name", sa.String(255), nullable=False)
    last_name = sa.Column("last_name", sa.String(255), nullable=False)
    birthday = sa.Column("birthday", sa.DATE, nullable=False)
    gender = sa.Column("gender", sa.Enum(enums.Genders), nullable=False)
    phone_number = sa.Column("phone_number", sa.VARCHAR(15), nullable=False)


class Admin(AbstractUser):
    __tablename__ = "admins"


class User(AbstractUser):
    __tablename__ = "users"


class Customer(AbstractUserProfile):
    __tablename__ = "customers"


class Seller(AbstractUserProfile):
    __tablename__ = "sellers"


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    email = sa.Column("email", sa.String(320), unique=True, nullable=False)
    name = sa.Column("name", sa.String(255), unique=True, nullable=False)
    country = sa.Column("country", sa.String(255), nullable=False)  # TODO: should be implemented as FK on Country
    phone_number = sa.Column("phone_number", sa.VARCHAR(15), nullable=False)
    mailing_address = sa.Column("mailing_address", sa.VARCHAR(1023), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    name = sa.Column("name", sa.String(255), unique=True, nullable=False)

    products = relationship(
        "Product",
        secondary="categories_to_products",
        back_populates="categories",
        lazy="subquery",
    )


class Product(Base):
    __tablename__ = "products"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    name = sa.Column("name", sa.String(255), unique=True, nullable=False)
    price = sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False)
    available_count = sa.Column("available_count", sa.Integer(), nullable=False, default=0)

    manufacturer_pk = sa.Column(
        "manufacturer_pk",
        sa.ForeignKey("manufacturers.pk", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )

    seller_sub = sa.Column(
        "seller_sub",
        sa.ForeignKey("sellers.user_sub", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )

    categories = relationship(
        "Category",
        secondary="categories_to_products",
        back_populates="products",
        lazy="subquery",
    )


class CategoryToProduct(Base):
    __tablename__ = "categories_to_products"
    __table_args__ = (sa.PrimaryKeyConstraint("category_pk", "product_pk"),)

    category_pk = sa.Column(
        "category_pk",
        sa.ForeignKey("categories.pk", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )
    product_pk = sa.Column(
        "product_pk",
        sa.ForeignKey("products.pk", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )


class Order(Base):
    __tablename__ = "orders"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    customer_sub = sa.Column(
        "customer_sub",
        sa.ForeignKey("customers.user_sub", ondelete="CASCADE"),
        nullable=False,
    )
    total_price = sa.Column("total_price", sa.DECIMAL(precision=10, scale=2), nullable=False)
    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "order_items"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    order_pk = sa.Column(
        "order_pk",
        sa.ForeignKey("orders.pk", ondelete="CASCADE"),
        nullable=False,
    )
    product_pk = sa.Column(
        "product_pk",
        sa.ForeignKey("products.pk", ondelete="CASCADE"),
        nullable=False,
    )
    quantity = sa.Column("quantity", sa.Integer(), nullable=False)
