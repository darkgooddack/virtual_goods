from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseSettings):
    secret_key: str
    algorithm: str
    access_expire_min: int
    refresh_expire_days: int


class DatabaseConfig(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class ApiConfig(BaseSettings):
    prefix: str = "/api/v1"


class Settings(BaseSettings):
    db: DatabaseConfig
    jwt: JwtConfig
    api: ApiConfig = ApiConfig()


    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def get_attr(name: str):
    return getattr(get_settings(), name)