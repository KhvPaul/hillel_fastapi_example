from typing import Any, Dict

from pydantic import BaseSettings, FilePath, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    SERVER_PORT: int

    LOG_LEVEL: str = "DEBUG"

    SECRET_KEY: bytes
    ALGORITHM: str

    DESCRIPTION_FILE: FilePath | None

    # database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "db"
    DATABASE_ENDPOINT: PostgresDsn | None

    DATABASE_MAX_CONNECTIONS: int = 10
    DATABASE_CONNECTION_RECYCLE: int = 3600

    @validator("DATABASE_ENDPOINT", pre=True)
    def assemble_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:  # noqa: N805
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    # redis
    REDIS_HOST: str = "redis_db"
    REDIS_PORT: int = 6379
    REDIS_URL: RedisDsn | None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:  # noqa: N805
        if isinstance(v, str):
            return v
        return RedisDsn.build(scheme="redis", host=values.get("REDIS_HOST"), port=str(values.get("REDIS_PORT")))

    class Config:
        case_sensitive = True

        # https://docs.pydantic.dev/usage/settings/
        # `.env.prod` takes priority over `.env`
        env_file = ".env", ".env.prod"


settings = Settings()
