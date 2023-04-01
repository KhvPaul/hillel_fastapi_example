import asyncio
import sys

from pydantic import EmailStr

from db.session import get_async_postgres_session
from managers.admin_manager import AdminModelManager
from pydentic_models import common as pyd_mod_common


admin = AdminModelManager()


async def create_super_user(email: EmailStr, password: str):
    async with get_async_postgres_session() as session_cls:
        await admin.create_user(pyd_mod_common.SignUpRequest(email=email, password=password), session_cls)


async def main():
    email: EmailStr = EmailStr(sys.argv[1])
    password: str = sys.argv[2]
    await create_super_user(email, password)
    print("Admin created successfully!")  # noqa: T201


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
