import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI News Curation Pipeline"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # SQLite Database
    DATABASE_URL: str = "sqlite:///./focus.db"

    # Celery Broker & Backend (SQLite for zero-dependency local dev)
    CELERY_BROKER_URL: str = "sqla+sqlite:///./celery_broker.sqlite"
    CELERY_RESULT_BACKEND: str = "db+sqlite:///./celery_backend.sqlite"

    # Media Storage
    STORAGE_TEMP_DIR: str = "./storage/temp"

    # External APIs
    SERPAPI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL: str = "nvidia/nemotron-3-ultra-550b-a55b"
    DEFAULT_LLM_PROVIDER: str = "nvidia_nemotron"  # "nvidia_nemotron" | "gemini"

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
