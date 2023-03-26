import contextlib
from datetime import datetime
from typing import AsyncIterator, Optional

import jwt
from redis.asyncio import ConnectionPool, Redis

from config import settings
from utils import exceptions as custom_exc
from logger import logger


def decode_user_access_token(access_token: str):  # TODO: move to helper class
    try:
        return jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_signature": False, "verify_exp": True},
        )
    except jwt.ExpiredSignatureError as ex:
        logger.warning(f"Error token validation: {repr(ex)}")
        raise custom_exc.ErrorTokenValidation()
    except Exception as ex:
        logger.warning(f"Could not validate credentials: {repr(ex)}")
        raise custom_exc.ErrorCredentialsValidation()


@contextlib.asynccontextmanager
async def init_redis_pool() -> AsyncIterator[Redis]:
    redis_pool = ConnectionPool.from_url(url=settings.REDIS_URL)
    redis_conn = Redis(connection_pool=redis_pool)
    try:
        yield redis_conn
    finally:
        await redis_conn.close()
        if redis_conn.connection:
            await redis_conn.connection.wait_closed()


async def redis_token_cash_set_access_token(access_token: str) -> Optional[bool]:
    payload = decode_user_access_token(access_token)
    async with init_redis_pool() as r_session:
        timeout = datetime.fromtimestamp(payload["exp"]) - datetime.utcnow()
        await r_session.hset("users", payload["sub"], access_token)
        await r_session.sadd(f"access_tokens:{payload['sub']}", access_token)
        await r_session.expire(f"access_tokens:{payload['sub']}", timeout)
        return True


async def redis_token_cash_check_access_token(access_token: str) -> bool:
    payload = decode_user_access_token(access_token)
    async with init_redis_pool() as r_session:
        if not payload:
            raise custom_exc.ErrorTokenValidation()
        if not await r_session.sismember(f"access_tokens:{payload['sub']}", access_token):
            raise custom_exc.ErrorTokenValidation()
        if not await r_session.ttl(f"access_tokens:{payload['sub']}"):
            raise custom_exc.ErrorTokenValidation()
        return True


async def redis_token_cash_make_expired(access_token: str) -> Optional[bool]:
    payload = decode_user_access_token(access_token)
    async with init_redis_pool() as r_session:
        return await r_session.srem(f"access_tokens:{payload['sub']}", access_token)
