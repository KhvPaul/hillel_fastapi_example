import hmac
import hashlib

from pydantic import EmailStr
from sqlalchemy.ext import asyncio as sa_asyncio

from config import settings
from db.db_api import admins as admins_db_api
from managers.base_manager import BaseModelManager


class AdminModelManager(BaseModelManager):
    _db_api = admins_db_api.AdminsDBAPI()

    @staticmethod
    def get_password_hash(password: str) -> str:
        return hmac.new(settings.SECRET_KEY, password.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def compare_hashes(cls, password: str, hashed_password: str) -> bool:
        return cls.get_password_hash(password) == hashed_password

    async def create_admin(
        self, email: EmailStr, password: str, session_cls: sa_asyncio.AsyncSession
    ) -> bool:
        data: dict = {"email": email, "password": self.get_password_hash(password)}
        await self._db_api.create(session_cls, data)
        return True
