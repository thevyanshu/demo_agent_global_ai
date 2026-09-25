
from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    llm_provider: str = "groq"

    groq_api_key: str
    groq_model: str = "openai/gpt-oss-120b"

    sqlite_db_path: str = "data/checkpoints.sqlite"

    deepeval_model: str = "qwen/qwen3.8-27b"
    deepeval_threshold: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
