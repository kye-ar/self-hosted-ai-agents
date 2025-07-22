"""Main application settings configuration"""

import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    """
    Main application configuration settings.
    
    This class handles all non-LLM provider specific settings including
    database, authentication, API configuration, and CORS settings.
    """
    
    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./app.db", 
        description="Database connection URL"
    )
    
    # Authentication Settings
    api_keys: List[str] = Field(
        default=["dev-key-123", "dev-key-456"], 
        description="List of valid API keys for authentication"
    )
    enable_auth: bool = Field(
        default=True, 
        description="Enable API key authentication"
    )

    # API Configuration
    debug: bool = Field(
        default=True, 
        description="Enable debug mode for development"
    )
    log_level: str = Field(
        default="INFO", 
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    enable_swagger: bool = Field(
        default=True, 
        description="Enable Swagger/OpenAPI documentation"
    )

    # CORS (Cross-Origin Resource Sharing) Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"], 
        description="List of allowed CORS origins"
    )
    
    # LLM Provider Selection
    llm_provider: str = Field(
        default="ollama", 
        description="Selected LLM provider (ollama, openai, etc.)"
    )

    @validator('log_level')
    def validate_log_level(cls, v):
        """
        Ensure log level is valid.
        
        Args:
            v: The log level value to validate
            
        Returns:
            str: The validated log level
            
        Raises:
            ValueError: If log level is not valid
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of: {', '.join(valid_levels)}")
        return v.upper()

    @validator('api_keys')
    def validate_api_keys(cls, v):
        """
        Ensure at least one API key is provided when authentication is enabled.
        
        Args:
            v: List of API keys
            
        Returns:
            List[str]: The validated API keys
            
        Raises:
            ValueError: If no API keys provided in production
        """
        if not v and not os.getenv('DEBUG', 'false').lower() == 'true':
            raise ValueError("At least one API key must be provided in production")
        return v

    class Config:
        """
        Pydantic configuration for settings loading.
        
        - env_file: Load settings from .env file
        - env_file_encoding: Use UTF-8 encoding for .env file
        - env_nested_delimiter: Use __ for nested environment variables
        - case_sensitive: Make environment variable names case insensitive
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = False
        env_prefix = "APP__"



app_settings = AppSettings()