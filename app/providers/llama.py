import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
import json

from .base import LLMProvider
from ..config.providers.llama import LlamaProviderSettings

class LlamaProvider(LLMProvider):
    """
    Concrete implementation of the Ollama/Llama models.
    """
    def __init__(self, settings: LlamaProviderSettings):
        super().__init__(settings)
        self.settings: LlamaProviderSettings = settings
        # Fix: Use consistent attribute naming throughout the class
        self._session: aiohttp.ClientSession = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.settings.timeout_seconds)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def generate_text(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        
        session = await self._get_session()

        # Build the request payload in Ollama's format
        request_data = {
            "model": self.settings.default_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature or self.settings.temperature,
                "top_p": self.settings.top_p,
                "repeat_penalty": self.settings.repeat_penalty,
            }
        }

        # Handle max_tokens parameter (num_predict for Ollama)
        if max_tokens is not None:
            request_data["options"]["num_predict"] = max_tokens
        else:
            request_data["options"]["num_predict"] = self.settings.num_predict

        # Additional provider-specific parameters
        if kwargs:
            request_data["options"].update(kwargs)
        
        try:
            # Make the HTTP request to Ollama
            url = f"{self.settings.api_base}/api/generate"

            async with session.post(url, json=request_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ConnectionError(
                        f"Ollama API returned status {response.status}: {error_text}"
                    )

                # Parse the response
                response_data = await response.json()

                # Extract the generated text from Ollama's response
                if "response" in response_data:
                    return response_data["response"]
                else:
                    raise ValueError(f"Unexpected response format: {response_data}")
        
        except asyncio.TimeoutError:
            # Fix: Add missing 'f' before the f-string
            raise TimeoutError(f"Request to Ollama timed out after {self.settings.timeout_seconds} seconds")
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
    
    async def validate_connection(self) -> bool:
        """
        Validate connection to Ollama by checking if it's running
        """
        try:
            session = await self._get_session()
            url = f"{self.settings.api_base}/api/tags"

            async with session.get(url) as response:
                # Fix: Correct typo "receieved" -> "received"
                # If a response is received, the service is running
                return response.status == 200

        except Exception:
            return False

    # Fix: Add 'async' keyword since this method uses 'await'
    async def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Ollama
        """
        session = await self._get_session()

        try:
            url = f"{self.settings.api_base}/api/tags"

            async with session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ConnectionError(
                        f"Failed to get models from Ollama: {response.status} - {error_text}"
                    )

                response_data = await response.json()

                if "models" in response_data:
                    return [model["name"] for model in response_data["models"]]
                else:
                    return []
                
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to get models from Ollama: {str(e)}")

    async def close(self):
        """
        Clean up the session when finished with the provider
        """
        # Fix: Add space between 'not' and 'self._session.closed'
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Support for 'async with' context manager"""
        # Fix: Add proper implementation for context manager entry
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting 'async with' block"""
        # Fix: Corrected typo "wuth" -> "with"
        await self.close()
