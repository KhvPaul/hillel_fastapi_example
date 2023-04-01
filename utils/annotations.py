from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext import asyncio as sa_asyncio

from db.session import get_async_postgres_session
from dependencies.auth import AuthHandler
from utils import redis_api as redis

user_auth_handler = AuthHandler()


async def get_async_db_session() -> sa_asyncio.AsyncSession:
    async with get_async_postgres_session() as session_cls:
        yield session_cls


async def get_sub(access_token: str = Header(...)):
    await redis.redis_token_cash_check_access_token(access_token)
    return user_auth_handler.get_sub_by_access_token(access_token)


AsyncSession = Annotated[sa_asyncio.AsyncSession, Depends(get_async_db_session)]
Sub = Annotated[str, Depends(get_sub)]
