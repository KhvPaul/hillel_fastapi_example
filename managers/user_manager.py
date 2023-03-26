import hmac
import hashlib

from sqlalchemy.ext import asyncio as sa_asyncio

from config import settings
from db.db_api import users as users_db_api
from db.models import models_base as db_models
from dependencies.user_auth import UserAuthHandler
from managers.base_manager import BaseModelManager
from pydentic_models import common as pyd_mod_common, users as pyd_mod_users
from utils import exceptions as custom_exc


class UserModelManager(BaseModelManager):
    _db_api = users_db_api.UsersDBAPI()
    _db_api_user_profiles = users_db_api.UserProfilesDBAPI()

    _auth_handler = UserAuthHandler()

    @staticmethod
    def get_password_hash(password: str) -> str:
        return hmac.new(settings.SECRET_KEY, password.encode("utf-8"), hashlib.sha256).hexdigest()

    @classmethod
    def compare_hashes(cls, password: str, hashed_password: str) -> bool:
        return cls.get_password_hash(password) == hashed_password

    async def create_user(
        self, sign_up_data: pyd_mod_common.SignUpRequest, session_cls: sa_asyncio.AsyncSession
    ) -> bool:
        data: dict = sign_up_data.dict()
        data.update({"password": self.get_password_hash(sign_up_data.password)})
        await self._db_api.create(session_cls, data)
        return True

    async def sign_in(self, sign_up_data: pyd_mod_common.SignUpRequest, session_cls: sa_asyncio.AsyncSession) -> dict:
        user: db_models.User = await self._db_api.retrieve(session_cls, [db_models.User.email == sign_up_data.email])
        if not user:
            raise custom_exc.InvalidUserCredentialsException()
        if not self.compare_hashes(sign_up_data.password, user.password):
            raise custom_exc.InvalidUserCredentialsException()
        access_token = self._auth_handler.generate_access_token(user)
        await self._auth_handler.save_access_token(access_token)
        return {"access_token": access_token, "token_type": "bearer"}

    async def log_out(self, access_token: str) -> None:
        return await self._auth_handler.make_access_token_expired(access_token)

    async def retrieve_user_profile(self, sub: str, session_cls: sa_asyncio.AsyncSession) -> db_models.UserProfile:
        return await self._db_api_user_profiles.retrieve(session_cls, [db_models.UserProfile.user_sub == sub])

    async def create_user_profile(
        self, sub: str, data: pyd_mod_users.UserProfileRequest, session_cls: sa_asyncio.AsyncSession
    ) -> None:
        return await self._db_api_user_profiles.create(session_cls, {**data.dict(), "user_sub": sub})
