import http
import typing as t

from fastapi import Body, FastAPI, Header, Security
from fastapi.responses import JSONResponse

from managers.customer_manager import CustomerModelManager
from pydentic_models import common as pyd_mod_common, users as pyd_mod_users
from utils import helpers
from utils.annotations import AsyncSession
from utils.security import get_sub_checker

OK = {"message": "OK"}
OK_RESPONSE = JSONResponse(content=OK, status_code=http.HTTPStatus.CREATED)
router = FastAPI(description=helpers.get_description_file(), docs_url="/docs")

customer = CustomerModelManager()


@router.post(
    "/sign_up/",
    response_model=pyd_mod_common.ResponseOk,
    tags=["Registration Authorization"],
)
async def sign_up(
    session_cls: AsyncSession,
    sign_up_data: pyd_mod_users.UserSignUpRequest = Body(...),
):
    return await customer.create_user(sign_up_data, session_cls)


@router.post(
    "/sign_in/",
    response_model=pyd_mod_common.SignUpResp,
    tags=["Registration Authorization"],
)
async def sign_in(
    session_cls: AsyncSession,
    sign_in_data: pyd_mod_common.SignUpRequest = Body(...),
):
    return await customer.sign_in(sign_in_data, session_cls)


@router.post(
    "/log_out/",
    response_model=pyd_mod_common.ResponseOk,
    tags=["Registration Authorization"],
)
async def log_out(id_token: str = Header(...)):
    await customer.log_out(id_token)
    return OK


@router.get("/get_profile/", tags=["User Profile"], response_model=t.Optional[pyd_mod_users.UserResponse])
async def get_profile(
    session_cls: AsyncSession,
    sub: str = Security(get_sub_checker, scopes=["customer"]),
):
    return await customer.retrieve_user(sub, session_cls)
