import hmac
import hashlib

from pydantic import EmailStr
from sqlalchemy.ext import asyncio as sa_asyncio

from config import settings
from db.db_api import admins as admins_db_api
from db.models import models_base as db_models
from dependencies.user_auth import UserAuthHandler
from managers.base_manager import BaseModelManager
from utils import exceptions as custom_exc


class AdminModelManager(BaseModelManager):
    _db_api = admins_db_api.AdminsDBAPI()

    _auth_handler = UserAuthHandler()

    @staticmethod
    def get_password_hash(password: str) -> str:
        return hmac.new(settings.SECRET_KEY, password.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def compare_hashes(cls, password: str, hashed_password: str) -> bool:
        return cls.get_password_hash(password) == hashed_password

    async def create_admin(self, email: EmailStr, password: str, session_cls: sa_asyncio.AsyncSession) -> bool:
        data: dict = {"email": email, "password": self.get_password_hash(password)}
        await self._db_api.create(session_cls, data)
        return True

    async def sign_in(self, email: EmailStr, password, session_cls: sa_asyncio.AsyncSession) -> dict:
        admin: db_models.Admin = await self._db_api.retrieve(session_cls, [db_models.Admin.email == email])
        if not admin:
            raise custom_exc.InvalidUserCredentialsException()
        if not self.compare_hashes(password, admin.password):
            raise custom_exc.InvalidUserCredentialsException()
        access_token = self._auth_handler.generate_access_token(admin)
        await self._auth_handler.save_access_token(access_token)
        return {"access_token": access_token, "token_type": "bearer"}

    async def sign_in_session(self, email: EmailStr, password, session_cls: sa_asyncio.AsyncSession) -> str:
        res = await self.sign_in(email, password, session_cls)
        return res.get("access_token")

    async def log_out(self, access_token: str) -> None:
        return await self._auth_handler.make_access_token_expired(access_token)
