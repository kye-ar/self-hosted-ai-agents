import asyncio
import sys
import os
import time
import psutil
from typing import List, Dict, Any

# Add the parent directory to Python path and change working directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(parent_dir))
os.chdir(os.path.dirname(parent_dir))

from app.providers.llama import LlamaProvider
from app.config.providers.llama import LlamaProviderSettings

class StressTestMetrics:
    """Track metrics during stress testing"""
    def __init__(self):
        self.requests_sent = 0
        self.requests_successful = 0
        self.requests_failed = 0
        self.total_response_time = 0.0
        self.min_response_time = float('inf')
        self.max_response_time = 0.0
        self.errors = []
        self.start_memory = 0
        self.peak_memory = 0

    def add_request(self, success: bool, response_time: float, error: str = None):
        self.requests_sent += 1
        if success:
            self.requests_successful += 1
            self.total_response_time += response_time
            self.min_response_time = min(self.min_response_time, response_time)
            self.max_response_time = max(self.max_response_time, response_time)
        else:
            self.requests_failed += 1
            if error:
                self.errors.append(error)

    def get_average_response_time(self) -> float:
        if self.requests_successful == 0:
            return 0.0
        return self.total_response_time / self.requests_successful

    def get_success_rate(self) -> float:
        if self.requests_sent == 0:
            return 0.0
        return (self.requests_successful / self.requests_sent) * 100

async def single_request_test(provider: LlamaProvider, prompt: str, request_id: int) -> Dict[str, Any]:
    """Perform a single request and track metrics"""
    start_time = time.time()
    
    try:
        response = await provider.generate_text(prompt, max_tokens=20)
        end_time = time.time()
        
        return {
            'success': True,
            'response_time': end_time - start_time,
            'response_length': len(response),
            'request_id': request_id,
            'error': None
        }
    except Exception as e:
        end_time = time.time()
        return {
            'success': False,
            'response_time': end_time - start_time,
            'response_length': 0,
            'request_id': request_id,
            'error': str(e)
        }

async def concurrent_requests_test(num_requests: int = 10, max_concurrent: int = 5):
    """Test multiple concurrent requests"""
    print(f"🔥 Testing {num_requests} concurrent requests (max {max_concurrent} at once)...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
        timeout_seconds=30
    )
    
    metrics = StressTestMetrics()
    metrics.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    # Prepare test prompts
    prompts = [
        "What is the capital of France?",
        "Count from 1 to 5",
        "Write a short joke",
        "What is 2+2?",
        "Name three colors",
        "Say hello in Spanish",
        "What day comes after Monday?",
        "Name a programming language",
        "What is the opposite of hot?",
        "Write one word"
    ]
    
    async with LlamaProvider(settings) as provider:
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_request(request_id: int):
            async with semaphore:
                prompt = prompts[request_id % len(prompts)]
                return await single_request_test(provider, prompt, request_id)
        
        # Execute requests
        start_time = time.time()
        tasks = [bounded_request(i) for i in range(num_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                metrics.add_request(False, 0.0, str(result))
            else:
                metrics.add_request(
                    result['success'], 
                    result['response_time'], 
                    result.get('error')
                )
            
            # Track memory usage
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            metrics.peak_memory = max(metrics.peak_memory, current_memory)
    
    # Print results
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Requests per second: {num_requests / total_time:.2f}")
    print(f"  Success rate: {metrics.get_success_rate():.1f}%")
    print(f"  Average response time: {metrics.get_average_response_time():.2f}s")
    print(f"  Min response time: {metrics.min_response_time:.2f}s")
    print(f"  Max response time: {metrics.max_response_time:.2f}s")
    print(f"  Memory usage: {metrics.start_memory:.1f}MB → {metrics.peak_memory:.1f}MB")
    
    if metrics.errors:
        print(f"  Errors ({len(metrics.errors)}):")
        for error in set(metrics.errors[:5]):  # Show unique errors, max 5
            print(f"    - {error}")
    
    return metrics.get_success_rate() > 80  # Pass if >80% success rate

async def sustained_load_test(duration_seconds: int = 60, requests_per_second: int = 2):
    """Test sustained load over time"""
    print(f"⏱️  Testing sustained load: {requests_per_second} req/s for {duration_seconds}s...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
        timeout_seconds=15
    )
    
    metrics = StressTestMetrics()
    metrics.start_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    prompts = ["Quick response test", "Fast answer needed", "Brief reply please"]
    
    async with LlamaProvider(settings) as provider:
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < duration_seconds:
            batch_start = time.time()
            
            # Send batch of requests
            tasks = []
            for _ in range(requests_per_second):
                prompt = prompts[request_count % len(prompts)]
                tasks.append(single_request_test(provider, prompt, request_count))
                request_count += 1
            
            # Execute batch
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    metrics.add_request(False, 0.0, str(result))
                else:
                    metrics.add_request(
                        result['success'], 
                        result['response_time'], 
                        result.get('error')
                    )
                
                # Track memory
                current_memory = psutil.Process().memory_info().rss / 1024 / 1024
                metrics.peak_memory = max(metrics.peak_memory, current_memory)
            
            # Wait for next second
            batch_time = time.time() - batch_start
            if batch_time < 1.0:
                await asyncio.sleep(1.0 - batch_time)
    
    actual_duration = time.time() - start_time
    
    print(f"  Actual duration: {actual_duration:.1f}s")
    print(f"  Total requests: {metrics.requests_sent}")
    print(f"  Actual req/s: {metrics.requests_sent / actual_duration:.2f}")
    print(f"  Success rate: {metrics.get_success_rate():.1f}%")
    print(f"  Average response time: {metrics.get_average_response_time():.2f}s")
    print(f"  Memory growth: {metrics.peak_memory - metrics.start_memory:.1f}MB")
    
    if metrics.errors:
        error_types = {}
        for error in metrics.errors:
            error_type = error.split(':')[0] if ':' in error else error
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        print(f"  Error types:")
        for error_type, count in error_types.items():
            print(f"    - {error_type}: {count}")
    
    return metrics.get_success_rate() > 75  # Pass if >75% success rate

async def memory_leak_test(num_iterations: int = 50):
    """Test for memory leaks with many provider instances"""
    print(f"🧠 Testing for memory leaks over {num_iterations} iterations...")
    
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
    )
    
    initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
    memory_samples = [initial_memory]
    
    for i in range(num_iterations):
        async with LlamaProvider(settings) as provider:
            # Generate a small response
            await provider.generate_text("Test", max_tokens=5)
        
        # Sample memory every 10 iterations
        if i % 10 == 0:
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory)
            print(f"  Iteration {i}: {current_memory:.1f}MB")
    
    final_memory = psutil.Process().memory_info().rss / 1024 / 1024
    memory_growth = final_memory - initial_memory
    
    print(f"  Initial memory: {initial_memory:.1f}MB")
    print(f"  Final memory: {final_memory:.1f}MB")
    print(f"  Memory growth: {memory_growth:.1f}MB")
    
    # Pass if memory growth is reasonable (< 50MB for 50 iterations)
    acceptable_growth = num_iterations  # 1MB per iteration is acceptable
    return memory_growth < acceptable_growth

async def timeout_stress_test():
    """Test behavior under timeout conditions"""
    print("⏰ Testing timeout handling...")
    
    # Use very short timeout to force timeouts
    settings = LlamaProviderSettings(
        api_base="http://host.docker.internal:11434",
        default_model="llama3.2:latest",
        timeout_seconds=1  # Very short timeout
    )
    
    timeout_count = 0
    success_count = 0
    
    async with LlamaProvider(settings) as provider:
        # Try 10 requests with very short timeout
        for i in range(10):
            try:
                response = await provider.generate_text(
                    "Write a very long detailed story about adventures in space with many characters and plot twists",
                    max_tokens=200  # Request long response
                )
                success_count += 1
                print(f"  Request {i+1}: Success (unexpected!)")
            except Exception as e:
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    timeout_count += 1
                    print(f"  Request {i+1}: Timeout (expected)")
                else:
                    print(f"  Request {i+1}: Other error - {e}")
    
    print(f"  Timeouts: {timeout_count}/10")
    print(f"  Successes: {success_count}/10")
    
    # Pass if we got some timeouts (showing timeout handling works)
    return timeout_count > 0

async def run_stress_tests():
    """Run all stress tests"""
    print("🔥 Starting Llama Provider Stress Tests\n")
    
    tests = [
        ("Concurrent Requests (Light)", lambda: concurrent_requests_test(10, 3)),
        ("Concurrent Requests (Heavy)", lambda: concurrent_requests_test(20, 5)),
        ("Sustained Load", lambda: sustained_load_test(30, 2)),
        ("Memory Leak Test", lambda: memory_leak_test(30)),
        ("Timeout Stress", timeout_stress_test),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            start_time = time.time()
            result = await test_func()
            duration = time.time() - start_time
            
            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"Result: {status} (took {duration:.1f}s)")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results[test_name] = False
        
        # Brief pause between tests
        await asyncio.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("STRESS TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} stress tests passed")
    
    if passed == total:
        print("🚀 All stress tests passed! Your Llama provider is robust!")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Your provider may need optimization.")

if __name__ == "__main__":
    asyncio.run(run_stress_tests())