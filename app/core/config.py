from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    model_config = ConfigDict(env_file = ".env")


@lru_cache
def get_settings():
    return Settings()
