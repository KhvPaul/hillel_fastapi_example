import http
import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from admin.admin_interface import AdminApplicationBuilder
from config import settings
from pydentic_models.common import ResponseOk
from routers import customer_controllers, seller_controllers
from utils import annotations, helpers

OK = {"message": "OK"}
OK_RESPONSE = JSONResponse(content=OK, status_code=http.HTTPStatus.OK)

app = FastAPI(description=helpers.get_description_file(), docs_url="/")
app = AdminApplicationBuilder(app)()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.mount("/api/v1/customer", customer_controllers.router, "customer")
app.mount("/api/v1/seller", seller_controllers.router, "seller")


@app.get(
    "/ping/",
    tags=["Test Db Connection"],
    response_model=ResponseOk,
    summary="Database healthcheck endpoint",
    description="Sends a dummy request to the database to connect. \
                Required to verify the connection to the database \
                of working outside the docker network",
)
async def ping(session_cls: annotations.AsyncSession):
    from db.db_api.base import DBApiBase

    await DBApiBase().ping(session_cls)
    return OK_RESPONSE


if __name__ == "__main__":
    server = Server(
        Config(
            app,
            host="0.0.0.0",
            port=settings.SERVER_PORT,
            workers=int(os.getenv("WORKERS", 1)),
            loop="uvloop",
        ),
    )
    server.run()
