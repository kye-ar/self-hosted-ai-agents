
import asyncio
import sys
import os

# Add the parent directory to Python path and change working directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(parent_dir))
os.chdir(os.path.dirname(parent_dir))

# Now we can import as if we're running from the project root
from app.providers.llama import LlamaProvider
from app.config.providers.llama import LlamaProviderSettings

async def test_basic_functionality():
    """Simple test to verify the provider works"""
    print("🧪 Testing Llama Provider")
    
    # Configure to connect to host machine Ollama
    # host.docker.internal allows Docker to reach your host machine
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",  # Change to your model
        max_tokens=50
    )
    
    async with LlamaProvider(settings) as provider:
        # Test connection
        print("🔍 Testing connection...")
        connected = await provider.validate_connection()
        print(f"Connected: {connected}")
        
        if connected:
            # Test text generation
            print("💬 Testing text generation...")
            response = await provider.generate_text("Say hello in one sentence.")
            print(f"Response: {response}")
        
        # Show health status
        health = await provider.health_check()
        print(f"Health: {health}")

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())