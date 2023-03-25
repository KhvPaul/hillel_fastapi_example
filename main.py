import http
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from config import settings
from pydentic_models.common import ResponseOk
from utils import annotations, helpers

OK = {"message": "OK"}
OK_RESPONSE = JSONResponse(content=OK, status_code=http.HTTPStatus.OK)

app = FastAPI(description=helpers.get_description_file(), docs_url="/")


@app.get("/ping/", tags=["Test Db Connection"], response_model=ResponseOk)
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
