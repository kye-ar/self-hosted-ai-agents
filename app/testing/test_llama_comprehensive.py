import asyncio
import sys
import os

# Add the parent directory to Python path and change working directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(parent_dir))
os.chdir(os.path.dirname(parent_dir))

from app.providers.llama import LlamaProvider
from app.config.providers.llama import LlamaProviderSettings

async def test_model_listing():
    """Test getting available models from Ollama"""
    print("🔍 Testing model listing...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
    )
    
    async with LlamaProvider(settings) as provider:
        try:
            models = await provider.get_available_models()
            print(f"Available models: {models}")
            return len(models) > 0
        except Exception as e:
            print(f"Error getting models: {e}")
            return False

async def test_parameter_variations():
    """Test different parameter settings"""
    print("🎛️  Testing parameter variations...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
    )
    
    test_cases = [
        {"prompt": "Count to 3", "max_tokens": 10, "temperature": 0.1},
        {"prompt": "Write a creative story opener", "max_tokens": 30, "temperature": 0.9},
        {"prompt": "What is 2+2?", "temperature": 0.0},  # Very deterministic
    ]
    
    async with LlamaProvider(settings) as provider:
        results = []
        for i, test_case in enumerate(test_cases):
            try:
                print(f"  Test {i+1}: {test_case['prompt'][:20]}...")
                response = await provider.generate_text(**test_case)
                print(f"  Response: {response[:50]}...")
                results.append(True)
            except Exception as e:
                print(f"  Error: {e}")
                results.append(False)
        
        return all(results)

async def test_longer_conversation():
    """Test a longer multi-turn conversation"""
    print("💬 Testing longer conversation...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
        max_tokens=100
    )
    
    conversation_prompts = [
        "Hello, can you tell me your name?",
        "What's the weather like on Mars?",
        "Write a haiku about coding",
    ]
    
    async with LlamaProvider(settings) as provider:
        responses = []
        for prompt in conversation_prompts:
            try:
                print(f"  Asking: {prompt}")
                response = await provider.generate_text(prompt, max_tokens=50)
                print(f"  Response: {response[:80]}...")
                responses.append(response)
            except Exception as e:
                print(f"  Error: {e}")
                return False
        
        return len(responses) == len(conversation_prompts)

async def test_error_handling():
    """Test error handling with invalid settings"""
    print("⚠️  Testing error handling...")
    
    # Test with invalid API base
    bad_settings = LlamaProviderSettings(
        api_base="http://nonexistent:11434",
        default_model="llama3.2:latest",
    )
    
    async with LlamaProvider(bad_settings) as provider:
        # This should return False for connection validation
        connected = await provider.validate_connection()
        print(f"  Connection to bad endpoint: {connected}")
        
        if connected:
            print("  ⚠️  Expected connection to fail but it didn't")
            return False
        else:
            print("  ✅ Correctly detected invalid endpoint")
            return True

async def test_context_manager():
    """Test that context manager properly cleans up"""
    print("🧹 Testing context manager cleanup...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
    )
    
    provider = LlamaProvider(settings)
    
    # Test manual context management
    await provider.__aenter__()
    
    # Generate some text to ensure session is created
    try:
        response = await provider.generate_text("Hello", max_tokens=5)
        print(f"  Generated: {response}")
        
        # Check if session exists
        session_exists = provider._session is not None
        print(f"  Session created: {session_exists}")
        
        # Clean up
        await provider.__aexit__(None, None, None)
        
        # Check if session is closed
        session_closed = provider._session.closed if provider._session else True
        print(f"  Session cleaned up: {session_closed}")
        
        return session_exists and session_closed
        
    except Exception as e:
        print(f"  Error: {e}")
        await provider.__aexit__(None, None, None)
        return False

async def run_comprehensive_tests():
    """Run all tests and report results"""
    print("🚀 Starting Comprehensive Llama Provider Tests\n")
    
    tests = [
        ("Model Listing", test_model_listing),
        ("Parameter Variations", test_parameter_variations),
        ("Longer Conversation", test_longer_conversation),
        ("Error Handling", test_error_handling),
        ("Context Manager", test_context_manager),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = await test_func()
            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"Result: {status}")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Llama provider is working great!")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())