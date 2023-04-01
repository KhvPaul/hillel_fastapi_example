from fastapi import Header
from fastapi.security import SecurityScopes

from dependencies.auth import AuthHandler
from utils import exceptions as custom_exc, redis_api as redis


user_auth_handler = AuthHandler()


class AccessChecker:
    async def __call__(self, statuses: dict, perm):
        for item in perm:
            if statuses[item] != "1":
                raise custom_exc.AccessDenied()


class AccessCheckerRole:
    async def __call__(self, role: str, perm):
        if role not in perm:
            raise custom_exc.AccessDenied()


check_status = AccessChecker()
check_role = AccessCheckerRole()


async def get_sub_checker(security_scopes: SecurityScopes, access_token: str = Header(...)):
    async def get_sub():
        await redis.redis_token_cash_check_access_token(access_token)
        await check_role(user_auth_handler.get_role_by_access_token(access_token), security_scopes.scopes)
        return user_auth_handler.get_sub_by_access_token(access_token)

    return await get_sub()
