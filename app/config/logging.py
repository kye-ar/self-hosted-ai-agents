""" Dedicated logging configuration """

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class LoggingSettings(BaseSettings):
    """
    Isolated logging configuration that handles all logging-related settings
    """
    # Basic settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default="logs/app.log", description="Log file location")

    # File rotation settings to prevent oversized log files
    log_max_sizes: int = Field(default=10485760, description="Maxmimum size of log file in bytes")
    log_backup_count: int = Field(default=5, description="Number of backup log files to keep")

    # Log format
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )

    # Output destinations
    log_to_console: bool = Field(default=True, description="Enable console logging")
    log_to_file: bool = Field(default=True, description="Enable file logging")

    @validator('log_level')
    def validate_log_level(cls, v):
        """
        Ensure log level is one of Python's standard logging levels.
        This catches configuration errors early rather than at runtime.
        """
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()

    class Config:
        env_prefix = "LOGGING__"

def setup_logging(settings: LoggingSettings):
    """ 
    Configure Python's Logging system based on the settings
    """

    # Create log directory if required
    if settings.log_to_file and settings.log_file:
        log_dir = os.path.dirname(settings.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}")

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level))

    # Clear existing handlers and avoid duplicate logging
    logger.handlers.clear()

    # Create a consistent formatter for all handlers
    formatter = logging.Formatter(settings.log_format)

    # Show logs in console, if enabled
    if settings.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        print(f"Console logging enabled at {settings.log_level} level")
    
    # Write logs to file, if enabled
    if settings.log_to_file and settings.log_file:
        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_sizes,
            backupCount=settings.log_backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(f"File logging enabled: {settings.log_file}")

def get_logger(name: str):
    """
    Convenience function to get a logger for a specific module
    """

    return logging.getLogger(name)

    