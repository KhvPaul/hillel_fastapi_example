import os

from fastapi import FastAPI
from uvicorn import Config, Server

from config import settings
from utils import helpers


app = FastAPI(description=helpers.get_description_file(), docs_url="/")


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
