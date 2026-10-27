from enum import StrEnum

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class TimetablesSettings(BaseModel):
    base_url: str
    client_id: str
    client_secret: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="forbid",
    )

    env: Environment
    debug: bool = False
    timetables: TimetablesSettings


settings = Settings()
