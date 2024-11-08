from sqlalchemy import Float, and_, cast, func, insert, select, update

from .database import Base, async_engine, async_session_factory
from .models import RatedAnimeModel, User


class AnimeORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def insert_new_user(telegram_id: int = None, username: str = None):
        async with async_session_factory() as session:
            user = {
                "telegram_id": telegram_id,
                "username": username,
            }
            query = insert(
                User,
            ).values(user)

            await session.execute(query)
            await session.commit()

    @staticmethod
    async def select_anime_rate_by_telegram_user(
        telegram_user_id: int, anime_id: int
    ):
        async with async_session_factory() as session:
            try:
                user_query = select(User).filter(
                    User.telegram_id == telegram_user_id
                )

                score_query = select(RatedAnimeModel.score).filter(
                    RatedAnimeModel.anime_id == anime_id,
                    RatedAnimeModel.user_id == user_query.c.id,
                )

                res = await session.execute(score_query)
                result = res.scalars().first()
                return result
            except:
                return None

    @staticmethod
    async def insert_anime_rate_by_user(anime_id: int, score: int, **kwargs):
        if len(kwargs.keys() & {"user_id", "telegram_user_id"}) != 1:
            raise ValueError(
                "One key argument is required MAX(1): [user_id,telegram_user_id]"
            )

        user_id = kwargs.get("user_id")

        if user_id is None:
            user_id = select(
                User.id,
            ).filter(User.telegram_id == kwargs.get("telegram_user_id"))

        rated_anime = {
            "anime_id": anime_id,
            "user_id": user_id,
            "score": score,
        }

        async with async_session_factory() as session:
            insert_anime = insert(RatedAnimeModel).values(rated_anime)

            await session.execute(insert_anime)

            await session.commit()

    @staticmethod
    async def update_anime_rate_by_user(score: int, anime_id: int, **kwargs):
        if len(kwargs.keys() & {"user_id", "telegram_user_id"}) != 1:
            raise ValueError(
                "One key argument is required MAX(1): [user_id,telegram_user_id]"
            )

        user_id = kwargs.get("user_id")

        async with async_session_factory() as session:
            if user_id is None:
                user_id = select(
                    User.id,
                ).filter(User.telegram_id == kwargs.get("telegram_user_id"))
                user_id = user_id.c.id

            stmt = (
                update(RatedAnimeModel)
                .filter(
                    and_(
                        RatedAnimeModel.anime_id == anime_id,
                        RatedAnimeModel.user_id == user_id,
                    )
                )
                .values({"score": score})
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def select_avg_anime_score(anime_id: int):
        async with async_session_factory() as session:
            query = (
                select(
                    RatedAnimeModel.anime_id,
                    cast(func.avg(RatedAnimeModel.score), Float).label(
                        "avg_score"
                    ),
                )
                .filter(
                    RatedAnimeModel.anime_id == anime_id,
                )
                .group_by(RatedAnimeModel.anime_id)
            )

            res = await session.execute(query)
            anime_id, avg_score = res.all()[0]

            return anime_id, avg_score
