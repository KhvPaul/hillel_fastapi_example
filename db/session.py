import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import asyncio as sa_asyncio

from config import settings

engine = create_engine(settings.DATABASE_ENDPOINT, pool_pre_ping=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextlib.asynccontextmanager
async def get_async_postgres_session() -> sa_asyncio.AsyncSession:
    engine = sa_asyncio.create_async_engine(
        settings.DATABASE_ENDPOINT,
        echo=False,
        pool_size=int(settings.DATABASE_MAX_CONNECTIONS) * 0.9,
        max_overflow=int(settings.DATABASE_MAX_CONNECTIONS) * 0.1,
        pool_recycle=int(settings.DATABASE_CONNECTION_RECYCLE),
    )
    async_session_cls = sessionmaker(bind=engine, class_=sa_asyncio.AsyncSession, expire_on_commit=False)
    yield async_session_cls
