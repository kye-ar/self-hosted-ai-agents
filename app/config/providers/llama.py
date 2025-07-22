""" Llama/Ollama specific configuration """

from typing import Dict, Any
from pydantic import Field, validator
from ..base import BaseLLMProviderSettings

class LlamaProviderSettings(BaseLLMProviderSettings):
    """
    Configuration specific to Llama models via Ollama
    """

    provider_name: str = Field("ollama", description="Provider name")
    api_base: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    default_model: str = Field(default="llama-3.2", description ="Default model to use")

    # Llama-specific parameters
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling parameter")
    repeat_penalty: float = Field(default=1.1, ge=0.0, le=2.0, description="Repetition penalty")
    num_predict: int = Field(default=1, description="Number of predictions to generate")

    # Ollama-specific parameters for performance and behaviour
    keep_alive: str = Field(default="5m", description="How long to keep model alive in memory")
    stream: bool = Field(default=False, description="Enable streaming responses")

    @validator('top_p')
    def validate_top_p(cls, v):
        """
        Llama-specific validation for top_p parameter.
        This ensures the value is valid for Llama models specifically.
        """
        if not 0.0 <= v <= 1.0:
            raise ValueError('top_p must be between 0.0 and 1.0')
        return v

    @validator('repeat_penalty')
    def validate_repeat_penalty(cls, v):
        """
        Validation for repeat_penalty, which is specific to Llama models.
        """
        if not 0.0 <= v <= 2.0:
            raise ValueError('repeat_penalty must be between 0.0 and 2.0')
        return v

    def get_api_params(self) -> Dict[str, Any]:
        """
        Returns Llama-specific API parameters formatted for Ollama API calls.
        
        This method encapsulates how to properly format parameters for the Ollama API,
        keeping this knowledge isolated to the Llama provider.
        """
        return {
            "model": self.default_model,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repeat_penalty": self.repeat_penalty,
                "num_predict": self.num_predict,
            },
            "keep_alive": self.keep_alive,
            "stream": self.stream
        }

    class Config:
        env_prefix = "LLAMA__"