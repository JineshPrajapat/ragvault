from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    REDIS_URL: str
    RABBITMQ_URL: str ="guest"

    DATABASE_URL: str

    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENAI_EMBEDDING_MODEL : str

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_EMBEDDING_MODEL: str= "models/embedding-001"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    APP_TOKEN: str
    BASE_URL: str
    LOCAL_UPLOAD_PATH: str

    class Config:
        env_file = ".env"

settings =Settings()