from __future__ import annotations

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    secret_key: str = Field(default="dev-secret-key", alias="SECRET_KEY")
    jwt_secret: str = Field(default="dev-jwt-secret", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    database_url: str = Field(
        default="sqlite:///./socialflow.db", alias="DATABASE_URL")
    redis_url: str = Field(
        default="redis://localhost:6379/0", alias="REDIS_URL")
    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="CORS_ORIGINS",
    )
    social_platform_mode: str = Field(
        default="mock", alias="SOCIAL_PLATFORM_MODE")
    storage_provider: str = Field(default="local", alias="STORAGE_PROVIDER")
    storage_path: str = Field(default="./storage", alias="STORAGE_PATH")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
