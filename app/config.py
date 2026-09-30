import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI News Curation Pipeline"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # SQLite Database
    DATABASE_URL: str = "sqlite:///./focus.db"

    # Celery & Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Media Storage
    STORAGE_TEMP_DIR: str = "./storage/temp"

    # External APIs
    SERPAPI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Live Laravel Integration (HTTP Webhook)
    LARAVEL_API_URL: str = ""
    LARAVEL_API_TOKEN: str = ""

    # Autonomous Publishing Mode
    AUTO_PUBLISH: bool = False  # Set True for fully autonomous pipeline (no human review)

    # Streamlit & Client base URL
    FASTAPI_BASE_URL: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def ensure_temp_dir(self) -> Path:
        """Ensure temporary storage path exists."""
        temp_path = Path(self.STORAGE_TEMP_DIR)
        temp_path.mkdir(parents=True, exist_ok=True)
        return temp_path


settings = Settings()
settings.ensure_temp_dir()
