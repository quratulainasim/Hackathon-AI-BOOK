"""
Latency Testing for AI-BOOK RAG Chatbot
Tests the response times for /ask, /upload, and /reindex endpoints
"""

import time
import requests
import statistics
from typing import List, Dict, Any
import json

# Configuration
BASE_URL = "http://localhost:8000"  # Update this to your backend URL
NUM_REQUESTS = 10  # Number of requests to make for each endpoint for statistical significance

def measure_endpoint_latency(endpoint: str, method: str = "GET", payload: Dict[str, Any] = None, num_requests: int = NUM_REQUESTS) -> List[float]:
    """
    Measure the latency of a specific endpoint
    Returns a list of response times in milliseconds
    """
    latencies = []

    for i in range(num_requests):
        try:
            start_time = time.time()

            if method.upper() == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method.upper() == "POST":
                if payload:
                    response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
                else:
                    response = requests.post(f"{BASE_URL}{endpoint}")
            elif method.upper() == "DELETE":
                response = requests.delete(f"{BASE_URL}{endpoint}")

            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)

            print(f"Request {i+1}/{num_requests}: {latency_ms:.2f}ms")

        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {e}")
            latencies.append(float('inf'))  # Mark as failed request

    return latencies

def test_ask_endpoint_latency():
    """Test the latency of the /ask endpoint"""
    print("\nTesting /ask endpoint latency...")

    # Prepare test payload
    test_payload = {
        "question": "What is the AI-BOOK RAG Chatbot?",
        "context": "The AI-BOOK RAG Chatbot is designed to help users ask questions about AI, robotics, and related topics."
    }

    latencies = measure_endpoint_latency("/ask", "POST", test_payload)

    # Calculate statistics
    valid_latencies = [lat for lat in latencies if lat != float('inf')]
    if valid_latencies:
        avg_latency = statistics.mean(valid_latencies)
        median_latency = statistics.median(valid_latencies)
        min_latency = min(valid_latencies)
        max_latency = max(valid_latencies)
        std_dev = statistics.stdev(valid_latencies) if len(valid_latencies) > 1 else 0

        print(f"\n/ask endpoint latency results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  Median: {median_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        print(f"  Std Dev: {std_dev:.2f}ms")
        print(f"  Success rate: {len(valid_latencies)}/{len(latencies)}")

        # Performance thresholds
        if avg_latency < 2000:  # 2 seconds
            print("  ✓ Average latency is acceptable (< 2s)")
        else:
            print("  ⚠ Average latency is high (>= 2s)")

        return {
            "avg": avg_latency,
            "median": median_latency,
            "min": min_latency,
            "max": max_latency,
            "std_dev": std_dev,
            "success_rate": len(valid_latencies) / len(latencies)
        }
    else:
        print("  ✗ All requests failed")
        return None

def test_upload_endpoint_latency():
    """Test the latency of the /upload endpoint"""
    print("\nTesting /upload endpoint latency...")

    # Create a small test file for upload
    test_file_content = "This is a test document for latency testing purposes.\n" * 10
    test_file_path = "test_latency_upload.txt"

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_file_content)

    latencies = []

    for i in range(NUM_REQUESTS):
        try:
            start_time = time.time()

            with open(test_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{BASE_URL}/upload", files=files)

            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)

            print(f"Upload {i+1}/{NUM_REQUESTS}: {latency_ms:.2f}ms")

        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            latencies.append(float('inf'))

    # Clean up test file
    import os
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    # Calculate statistics
    valid_latencies = [lat for lat in latencies if lat != float('inf')]
    if valid_latencies:
        avg_latency = statistics.mean(valid_latencies)
        median_latency = statistics.median(valid_latencies)
        min_latency = min(valid_latencies)
        max_latency = max(valid_latencies)
        std_dev = statistics.stdev(valid_latencies) if len(valid_latencies) > 1 else 0

        print(f"\n/upload endpoint latency results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  Median: {median_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        print(f"  Std Dev: {std_dev:.2f}ms")
        print(f"  Success rate: {len(valid_latencies)}/{len(latencies)}")

        # Performance thresholds
        if avg_latency < 5000:  # 5 seconds
            print("  ✓ Average latency is acceptable (< 5s)")
        else:
            print("  ⚠ Average latency is high (>= 5s)")

        return {
            "avg": avg_latency,
            "median": median_latency,
            "min": min_latency,
            "max": max_latency,
            "std_dev": std_dev,
            "success_rate": len(valid_latencies) / len(latencies)
        }
    else:
        print("  ✗ All requests failed")
        return None

def test_reindex_endpoint_latency():
    """Test the latency of the /reindex endpoint"""
    print("\nTesting /reindex endpoint latency...")

    # Note: Reindexing might take a long time, so we'll run fewer requests
    latencies = measure_endpoint_latency("/reindex", "POST", num_requests=3)

    # Calculate statistics
    valid_latencies = [lat for lat in latencies if lat != float('inf')]
    if valid_latencies:
        avg_latency = statistics.mean(valid_latencies)
        median_latency = statistics.median(valid_latencies)
        min_latency = min(valid_latencies)
        max_latency = max(valid_latencies)
        std_dev = statistics.stdev(valid_latencies) if len(valid_latencies) > 1 else 0

        print(f"\n/reindex endpoint latency results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  Median: {median_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        print(f"  Std Dev: {std_dev:.2f}ms")
        print(f"  Success rate: {len(valid_latencies)}/{len(latencies)}")

        # Performance thresholds (reindexing is expected to be slower)
        if avg_latency < 30000:  # 30 seconds
            print("  ✓ Average latency is acceptable (< 30s)")
        else:
            print("  ⚠ Average latency is high (>= 30s) - this might be expected for large datasets")

        return {
            "avg": avg_latency,
            "median": median_latency,
            "min": min_latency,
            "max": max_latency,
            "std_dev": std_dev,
            "success_rate": len(valid_latencies) / len(latencies)
        }
    else:
        print("  ✗ All requests failed")
        return None

def test_health_endpoint_latency():
    """Test the latency of the /health endpoint"""
    print("\nTesting /health endpoint latency...")

    latencies = measure_endpoint_latency("/health", "GET")

    # Calculate statistics
    valid_latencies = [lat for lat in latencies if lat != float('inf')]
    if valid_latencies:
        avg_latency = statistics.mean(valid_latencies)
        median_latency = statistics.median(valid_latencies)
        min_latency = min(valid_latencies)
        max_latency = max(valid_latencies)
        std_dev = statistics.stdev(valid_latencies) if len(valid_latencies) > 1 else 0

        print(f"\n/health endpoint latency results:")
        print(f"  Average: {avg_latency:.2f}ms")
        print(f"  Median: {median_latency:.2f}ms")
        print(f"  Min: {min_latency:.2f}ms")
        print(f"  Max: {max_latency:.2f}ms")
        print(f"  Std Dev: {std_dev:.2f}ms")
        print(f"  Success rate: {len(valid_latencies)}/{len(latencies)}")

        # Performance thresholds
        if avg_latency < 100:  # 100ms
            print("  ✓ Average latency is excellent (< 100ms)")
        else:
            print("  ⚠ Average latency is high (>= 100ms)")

        return {
            "avg": avg_latency,
            "median": median_latency,
            "min": min_latency,
            "max": max_latency,
            "std_dev": std_dev,
            "success_rate": len(valid_latencies) / len(latencies)
        }
    else:
        print("  ✗ All requests failed")
        return None

def run_latency_tests():
    """Run all latency tests"""
    print("Starting Latency Tests for AI-BOOK RAG Chatbot")
    print("=" * 60)
    print(f"Making {NUM_REQUESTS} requests to each endpoint for statistical significance")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)

    results = {}

    # Test health endpoint first to ensure the server is running
    health_result = test_health_endpoint_latency()
    if health_result and health_result["success_rate"] > 0.5:  # At least 50% success rate
        print("\n✓ Server is responsive, proceeding with other tests")
    else:
        print("\n✗ Server is not responding, stopping tests")
        return results

    # Test other endpoints
    results["ask"] = test_ask_endpoint_latency()
    results["upload"] = test_upload_endpoint_latency()
    results["reindex"] = test_reindex_endpoint_latency()

    # Summary
    print("\n" + "=" * 60)
    print("Latency Test Summary:")
    print("=" * 60)

    for endpoint, result in results.items():
        if result:
            print(f"{endpoint.upper()} endpoint:")
            print(f"  Average latency: {result['avg']:.2f}ms")
            print(f"  Success rate: {result['success_rate']:.2%}")
        else:
            print(f"{endpoint.upper()} endpoint: FAILED")

    return results

if __name__ == "__main__":
    run_latency_tests()