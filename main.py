import os

from fastapi import FastAPI
from uvicorn import Config, Server

from config import settings


app = FastAPI(disable_docs=True)


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
