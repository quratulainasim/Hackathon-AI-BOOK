"""
Test script for LLM integration with Gemini
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.llm_client import get_chatbot_response
from src.services.rag_pipeline import get_rag_response

def test_llm_connection():
    print("Testing LLM connection with Gemini...")

    try:
        # Test basic response
        test_prompt = "Hello, how are you?"
        response = get_chatbot_response(test_prompt)

        print(f"Input: {test_prompt}")
        print(f"Response: {response}")

        if response and len(response) > 0:
            print("✓ LLM responded successfully")
            return True
        else:
            print("✗ LLM returned empty response")
            return False

    except Exception as e:
        print(f"Error connecting to LLM: {e}")
        return False

def test_rag_pipeline():
    print("\nTesting RAG pipeline...")

    try:
        # Test RAG response without highlighted content
        user_question = "What is artificial intelligence?"
        rag_response = get_rag_response(user_question)

        print(f"User question: {user_question}")
        print(f"RAG response: {rag_response[:200]}...")  # First 200 chars

        if rag_response and len(rag_response) > 0:
            print("✓ RAG pipeline responded successfully")
            return True
        else:
            print("✗ RAG pipeline returned empty response")
            return False

    except Exception as e:
        print(f"Error in RAG pipeline: {e}")
        return False

def test_rag_with_context():
    print("\nTesting RAG with context...")

    try:
        # Test RAG response with highlighted content
        user_question = "Explain machine learning"
        highlighted_content = "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data."
        rag_response = get_rag_response(user_question, highlighted_content)

        print(f"User question: {user_question}")
        print(f"Highlighted content: {highlighted_content}")
        print(f"RAG response: {rag_response[:200]}...")  # First 200 chars

        if rag_response and len(rag_response) > 0:
            print("✓ RAG with context responded successfully")
            return True
        else:
            print("✗ RAG with context returned empty response")
            return False

    except Exception as e:
        print(f"Error in RAG with context: {e}")
        return False

def run_llm_tests():
    print("Starting LLM Integration Tests")
    print("=" * 50)

    tests = [
        ("LLM Connection Test", test_llm_connection),
        ("RAG Pipeline Test", test_rag_pipeline),
        ("RAG with Context Test", test_rag_with_context)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("LLM Integration Test Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall Result: {'PASS' if all_passed else 'FAIL'}")

    return all_passed

if __name__ == "__main__":
    run_llm_tests()