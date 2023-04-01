from pydantic import EmailStr
from sqlalchemy.ext import asyncio as sa_asyncio

from db.db_api import admins as admins_db_api
from managers.base_manager import BaseModelManager
from pydentic_models import common as pyd_mod_common


class AdminModelManager(BaseModelManager):
    _db_api = admins_db_api.AdminsDBAPI()

    async def sign_in_session(self, email: EmailStr, password, session_cls: sa_asyncio.AsyncSession) -> str:
        res = await self.sign_in(pyd_mod_common.SignUpRequest(email=email, password=password), session_cls)
        return res.get("access_token")
