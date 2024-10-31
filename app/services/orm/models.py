from typing import Annotated

from sqlalchemy import (ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]


class RatedAnimeModel(Base):
    __tablename__ = "rated_anime"
    id: Mapped[intpk]
    anime_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    score: Mapped[int]

    __table_args__ = (
        UniqueConstraint(
            "anime_id",
            "user_id",
        ),
    )
