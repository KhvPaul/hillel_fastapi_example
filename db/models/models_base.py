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


class Admin(Base):
    __tablename__ = "admins"

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


class User(Base):
    __tablename__ = "users"

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

    profile = relationship("UserProfile", uselist=False, viewonly=True)


class UserProfile(Base):
    __tablename__ = "user_profiles"

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
    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        "updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    @hybrid_property
    def email(self) -> str:
        return self.user.email

    user = relationship(
        "User",
        lazy="joined",
        foreign_keys=[user_sub],
        primaryjoin="User.sub == UserProfile.user_sub",
        viewonly=True,
        uselist=False,
    )
