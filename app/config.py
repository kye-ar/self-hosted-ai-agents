import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Authentication
    api_keys: List[str] = ["dev-key-123", "dev-key-456"]
    enable_auth: bool = True

    # API Settings
    debug: bool = True
    log_level: str = "INFO"
    enable_swagger: bool = True

    # CORS (Cross-Origin Resource Sharing)
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Enable comma separated values to become lists
        env_nested_delimiter = "__"

settings = Settings()