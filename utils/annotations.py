from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext import asyncio as sa_asyncio

from db.session import get_async_postgres_session


async def get_async_db_session() -> sa_asyncio.AsyncSession:
    async with get_async_postgres_session() as session_cls:
        yield session_cls

AsyncSession = Annotated[sa_asyncio.AsyncSession, Depends(get_async_db_session)]
