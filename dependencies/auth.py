import datetime
import hashlib
import hmac

import jwt

from config import settings
from db.models import models_base as db_models
from utils import exceptions as custom_exc, redis_api as redis
from logger import logger


class AuthHandler:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return hmac.new(settings.SECRET_KEY, password.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def compare_hashes(cls, password: str, hashed_password: str) -> bool:
        return cls.get_password_hash(password) == hashed_password

    @staticmethod
    def decode_user_access_token(access_token: str):
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

    @staticmethod
    def generate_access_token(user: db_models.AbstractUser):
        roles = {db_models.Customer: "customer", db_models.Seller: "seller"}
        token_payload = {"sub": user.sub, "role": roles[type(user)], "exp": datetime.datetime.now().timestamp() + 3600}
        return jwt.encode(token_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @classmethod
    def get_sub_by_access_token(cls, access_token: str) -> str:
        payload = cls.decode_user_access_token(access_token)
        return payload["sub"]

    @classmethod
    def get_role_by_access_token(cls, access_token: str) -> str:
        payload = cls.decode_user_access_token(access_token)
        return payload["role"]

    @staticmethod
    async def save_access_token(access_token: str):
        await redis.redis_token_cash_set_access_token(access_token)

    @staticmethod
    async def make_access_token_expired(access_token: str):
        await redis.redis_token_cash_make_expired(access_token)

    @staticmethod
    async def check_access_token_alive(access_token: str):
        await redis.redis_token_cash_check_access_token(access_token)
