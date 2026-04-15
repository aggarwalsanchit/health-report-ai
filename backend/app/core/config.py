# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Health Report AI"
    API_V1_STR: str = "/api"
    SECRET_KEY: str
    GEMINI_API_KEY: str
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_FILE_TYPES: set = {"pdf", "png", "jpg", "jpeg"}
    RATE_LIMIT: str = "5/minute"
    CORS_ORIGINS: list[str] = ["*"]  # Restrict in production

    class Config:
        env_file = ".env"


settings = Settings()
