from typing import Annotated
from .database import Base
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

intpk = Annotated[
    int, 
    mapped_column(primary_key=True)
]


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]


class RatedAnimeModel(Base):
    __tablename__ = 'rated_anime'
    id: Mapped[intpk]
    anime_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    score: Mapped[int]

    __table_args__ = (
        UniqueConstraint('anime_id', 'user_id', ),
    )

