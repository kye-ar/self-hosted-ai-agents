from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..config.base import BaseLLMProviderSettings

class LLMProvider(ABC):
    """
    Abstract base class that all LLM providers should inherit from.
    """

    def __init__(self, settings: BaseLLMProviderSettings):
        """
        Initilize the provider with its configuration.
        """
        self.settings = settings
        self._is_connected = False

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        The main method: generate text from a prompt.
        """
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Test if the LLM service connection is working.
        """
        pass

    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """
        Get the list of available models from the provider.
        """
        pass

    async def health_check(self) -> Dict[str, Any]:
        """
        Comprehensive health check utilising the abstract methods.
        """
        health_status = {
            "provider_name": self.settings.provider_name,
            "is_connected": False,
            "default_model": self.settings.default_model,
            "available_models": [],
            "error_message": None
        }

        try:
            # Utilise the abstract methods to gather information
            is_connected = await self.validate_connection()
            health_status["is_connected"] = is_connected
            self._is_connected = is_connected

            if is_connected:
                available_models = await self.get_available_models()
                health_status["available_models"] = available_models

                # Check if the configured model is available
                if self.settings.default_model not in available_models:
                    health_status["error_message"] = (
                        f"Default model '{self.settings.default_model}' "
                        f"not found in available models"
                    )

        except Exception as e:
            health_status["error_message"] = str(e)
            self._is_connected = False

        return health_status

    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get the basic provider information.
        """
        return {
            "provider_name": self.settings.provider_name,
            "api_base": self.settings.api_base,
            "default_model": self.settings.default_model,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "timeout_seconds": self.settings.timeout_seconds
        }
    
    @property
    def is_connected(self) -> bool:
        """
        Property to check if the provider is connected.
        """
        return self._is_connected
