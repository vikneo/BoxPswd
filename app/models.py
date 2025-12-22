from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)
from sqlalchemy.types import Boolean, Integer, String


class Base(DeclarativeBase):
    """
    Docstring for Base
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        autoincrement=True,
    )


class User(Base):

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, nullable=True)
    boxpasses: Mapped[List["BoxPass"]] = relationship(
        lazy="joined",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}: - {self.login}"

    @validates("password")
    def valid_password(self, key, value):
        print(key, value)
        return value


class BoxPass(Base):

    __tablename__ = "boxpass"

    name_site: Mapped[str] = mapped_column(String(150), default="", nullable=True)
    link: Mapped[str] = mapped_column(String(500), nullable=False)
    login: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    pincode: Mapped[str] = mapped_column(String(10), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped[User] = relationship(back_populates="boxpasses")

    def __repr__(self) -> str:
        return f"{self.user_id} - {self.name_site}"
