from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, ForeignKey
from typing import List



class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    passwords: Mapped[List["Password"]] = relationship(
        "Password",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Password(Base):
    __tablename__ = 'passwords'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    encrypted_pwd: Mapped[str] = mapped_column(nullable=False)
    salt: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="passwords",
        lazy="joined"
    )
