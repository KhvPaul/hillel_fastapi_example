import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from pydentic_models import enums

Base = declarative.declarative_base()

_uuid = lambda: uuid.uuid4().hex  # noqa future workpiece for function
generate_uuid = lambda: _uuid()  # noqa


class UserModelMixin(Base):
    """ Abstract class that can't be initialized. Used to provide default User attrs (sub, email, password, etc.) """

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

    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        "updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class UserProfileModelMixin(Base):
    """
    Abstract class that can't be initialized. Used to provide default UserProfile attrs (first_name, last_name, etc)
    """

    __abstract__ = True

    first_name = sa.Column("first_name", sa.String(255), nullable=False)
    last_name = sa.Column("last_name", sa.String(255), nullable=False)
    birthday = sa.Column("birthday", sa.DATE, nullable=False)
    gender = sa.Column("gender", sa.Enum(enums.Genders), nullable=False)
    phone_number = sa.Column("phone_number", sa.VARCHAR(15), nullable=False)


class Admin(UserModelMixin):
    __tablename__ = "admins"


class Customer(UserModelMixin, UserProfileModelMixin):
    __tablename__ = "customers"


class Seller(UserModelMixin, UserProfileModelMixin):
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
