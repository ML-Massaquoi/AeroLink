from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AeroLink"
    app_env: str = "development"

    secret_key: str = "insecure-dev-key-change-me"
    session_cookie_name: str = "aerolink_session"
    session_max_age_seconds: int = 8 * 60 * 60

    database_url: str = "postgresql+psycopg://aerolink:aerolink@localhost:5432/aerolink"

    cors_origins: str = "http://localhost:3000"

    seed_admin_email: str | None = None
    seed_admin_password: str | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_test(self) -> bool:
        return self.app_env == "test"


@lru_cache
def get_settings() -> Settings:
    return Settings()
