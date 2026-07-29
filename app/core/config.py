from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(alias="APP_NAME")
    debug: bool = Field(alias="DEBUG")
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    database_url: str = Field(alias="DATABASE_URL")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(alias="OPENAI_MODEL")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
