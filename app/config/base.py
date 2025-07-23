"""Base configuration class that all LLM providers should inherit from"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class BaseLLMProviderSettings(BaseSettings, ABC):
    """
    Abstract base class for all LLM provider configurations.
    """
    # Required fields
    provider_name: str = Field(..., description="LLM provider name")
    api_base: str = Field(..., description="API base URL")
    default_model: str = Field(..., description="Default model to use")

    # Common parameters
    max_tokens: int = Field(default=2048, description="Maximum tokens for responses")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Response creativity")
    timeout_seconds: int = Field(default=60, description="API request timeout")

    @validator('temperature')
    def validate_temperature(cls, v):
        """
        Ensure temperature is within valid range
        """
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
    
    @abstractmethod
    def get_api_params(self) -> Dict[str, Any]:
        """
        Abstract method required by each provider.
        Returns the provider-specific params formatted for the API.
        """
        pass

    class Config:
        env_file = ".env"
        case_sensitive = False