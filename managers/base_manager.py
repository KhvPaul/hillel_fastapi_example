from sqlalchemy.ext import asyncio as sa_asyncio

from db.db_api import base as base_db_api
from db.models import models_base as db_models
from dependencies.auth import AuthHandler
from pydentic_models import common as pyd_mod_common
from utils import exceptions as custom_exc


class BaseModelManager:
    """
    Base class used to manage models
    """

    _db_api = base_db_api.DBApiBase()

    _auth_handler = AuthHandler()

    async def create_user(
        self, sign_up_data: pyd_mod_common.SignUpRequest, session_cls: sa_asyncio.AsyncSession
    ) -> bool:
        data: dict = sign_up_data.dict()
        data.update({"password": self._auth_handler.get_password_hash(sign_up_data.password)})
        await self._db_api.create(session_cls, data)
        return True

    async def sign_in(self, sign_up_data: pyd_mod_common.SignUpRequest, session_cls: sa_asyncio.AsyncSession) -> dict:
        user: db_models.AbstractUser = await self._db_api.retrieve(
            session_cls, [self._db_api.model.email == sign_up_data.email]
        )
        if not user:
            raise custom_exc.InvalidUserCredentialsException()
        if not self._auth_handler.compare_hashes(sign_up_data.password, user.password):
            raise custom_exc.InvalidUserCredentialsException()
        access_token = self._auth_handler.generate_access_token(user)
        await self._auth_handler.save_access_token(access_token)
        return {"access_token": access_token, "token_type": "bearer"}

    async def log_out(self, access_token: str) -> None:
        return await self._auth_handler.make_access_token_expired(access_token)

    async def retrieve_user(self, sub: str, session_cls: sa_asyncio.AsyncSession) -> db_models.AbstractUser:
        return await self._db_api.retrieve(session_cls, [self._db_api.model.sub == sub])
