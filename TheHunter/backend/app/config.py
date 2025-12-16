from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "The Hunter API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database - use environment variable if available, fallback to SQLite
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hunter.db")
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Allow all origins for now (dev mode)
    # In production, restrict to specific domains
    ALLOWED_ORIGINS: list = [
        "*"  # Allow all origins - will be restricted in production
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

