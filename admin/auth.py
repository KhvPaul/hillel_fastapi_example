from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from db.session import get_async_postgres_session
from managers.admin_manager import AdminModelManager
from utils import redis_api as redis

admin_manager = AdminModelManager()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        async with get_async_postgres_session() as session_cls:
            token = await admin_manager.sign_in_session(username, password, session_cls)
            request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        request.session.clear()
        await admin_manager.log_out(token)
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")
        if not token or not await redis.redis_token_cash_check_access_token(token):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
