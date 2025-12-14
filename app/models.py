from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, LargeBinary, String


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
    boxpasses: Mapped[List["BoxPass"]] = relationship(
        lazy="joined",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}: - {self.login}"


class BoxPass(Base):

    __tablename__ = "boxpass"

    logo: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    link: Mapped[str] = mapped_column(String(500), nullable=False)
    login: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped[User] = relationship(back_populates="boxpasses")

    def __repr__(self) -> str:
        return f"{self.user_id} - {self.link}"
