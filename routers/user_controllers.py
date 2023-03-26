import http
import typing as t

from fastapi import Body, FastAPI, Header
from fastapi.responses import JSONResponse

from managers.user_manager import UserModelManager
from pydentic_models import common as pyd_mod_common, users as pyd_mod_users
from utils import helpers
from utils.annotations import AsyncSession, Sub


OK = {"message": "OK"}
OK_RESPONSE = JSONResponse(content=OK, status_code=http.HTTPStatus.CREATED)
router = FastAPI(description=helpers.get_description_file(), docs_url="/docs")

user = UserModelManager()


@router.post(
    "/sign_up/",
    response_model=pyd_mod_common.ResponseOk,
    tags=["Registration Authorization"],
)
async def sign_up(
    session_cls: AsyncSession,
    sign_up_data: pyd_mod_common.SignUpRequest = Body(...),
):
    return await user.create_user(sign_up_data, session_cls)


@router.post(
    "/sign_in/",
    response_model=pyd_mod_common.SignUpResp,
    tags=["Registration Authorization"],
)
async def sign_in(
    session_cls: AsyncSession,
    sign_in_data: pyd_mod_common.SignUpRequest = Body(...),
):
    return await user.sign_in(sign_in_data, session_cls)


@router.post(
    "/log_out/",
    response_model=pyd_mod_common.ResponseOk,
    tags=["Registration Authorization"],
)
async def log_out(id_token: str = Header(...)):
    await user.log_out(id_token)
    return OK


@router.get("/get_profile/", tags=["User Profile"], response_model=t.Optional[pyd_mod_users.UserProfileResponse])
async def get_profile(
    sub: Sub,
    session_cls: AsyncSession,
):
    return await user.retrieve_user_profile(sub, session_cls)


@router.post("/create_profile/", tags=["User Profile"], response_model=pyd_mod_common.ResponseOk)
async def create_user_profile(
    sub: Sub,
    data: pyd_mod_users.UserProfileRequest,
    session_cls: AsyncSession,
):
    await user.create_user_profile(sub, data, session_cls)
    return OK
