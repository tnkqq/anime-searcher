from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine(
    echo = True,
    url=settings.DATABASE_URL_asyncpg,
    pool_size=5,
    max_overflow=10,
)


async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
