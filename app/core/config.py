from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    url: str = "redis://localhost:6379/0"
    broker_url: str = "redis://localhost:6379/1"
    backend_url: str = "redis://localhost:6379/2"


class JwtConfig(BaseSettings):
    secret_key: str = "test-secret-key"
    algorithm: str = "HS256"
    access_expire_min: int = 15
    refresh_expire_days: int = 7


class DatabaseConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    name: str = "test_db"
    user: str = "test_user"
    password: str = "test_password"

    @property
    def url(self) -> str:
        return (f"postgresql+asyncpg://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}")


class ApiConfig(BaseSettings):
    prefix: str = "/api/v1"


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    jwt: JwtConfig = JwtConfig()
    api: ApiConfig = ApiConfig()
    redis: RedisConfig = RedisConfig()

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
