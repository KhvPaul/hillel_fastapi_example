from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_PORT: int

    LOG_LEVEL: str = "DEBUG"

    class Config:
        case_sensitive = True

        # https://docs.pydantic.dev/usage/settings/
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"


settings = Settings()
