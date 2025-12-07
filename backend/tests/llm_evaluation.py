"""
LLM Answer Correctness Evaluation for AI-BOOK RAG Chatbot
Evaluates the quality and correctness of responses from Gemini 2.5 Flash
"""

import os
import sys
import json
from typing import List, Dict, Tuple
import asyncio
from dotenv import load_dotenv

# Add the backend src directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from backend.src.services.llm_client import get_chatbot_response
from backend.src.services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME

load_dotenv()

# Define test cases with expected answers or criteria
TEST_CASES = [
    {
        "question": "What is the main purpose of the AI-BOOK RAG Chatbot?",
        "expected_topics": ["AI", "questions", "help", "book", "artificial intelligence"],
        "context": "The AI-BOOK RAG Chatbot is designed to help users ask questions about AI, robotics, and related topics."
    },
    {
        "question": "Explain the RAG system in simple terms",
        "expected_topics": ["retrieval", "augmented", "generation", "documents", "context"],
        "context": "RAG stands for Retrieval-Augmented Generation. It retrieves relevant documents and uses them as context for generating responses."
    },
    {
        "question": "How does the system handle document uploads?",
        "expected_topics": ["upload", "documents", "processing", "storage"],
        "context": "The system allows users to upload documents which are then processed, chunked, and stored in vector format for retrieval."
    },
    {
        "question": "What technology powers the question answering?",
        "expected_topics": ["Gemini", "LLM", "AI", "model"],
        "context": "The system uses Gemini 2.5 Flash through the OpenAI Agent SDK for question answering capabilities."
    }
]

def evaluate_response_relevance(response: str, expected_topics: List[str]) -> float:
    """
    Evaluate how relevant the response is to the expected topics
    Returns a score between 0 and 1
    """
    response_lower = response.lower()
    matched_topics = 0

    for topic in expected_topics:
        if topic.lower() in response_lower:
            matched_topics += 1

    return matched_topics / len(expected_topics) if expected_topics else 0

def evaluate_response_coherence(response: str) -> float:
    """
    Evaluate the coherence and readability of the response
    Returns a score between 0 and 1
    """
    # Basic heuristics for coherence
    score = 1.0

    # Check if response is too short
    if len(response.strip()) < 10:
        return 0.2

    # Check for common coherence issues
    if response.count('?') > 3:  # Too many questions
        score -= 0.2
    if response.count('...') > 2:  # Too many ellipses
        score -= 0.2
    if response.count('__') > 0 or response.count('N/A') > 0:  # Placeholders
        score -= 0.3

    # Ensure minimum score
    return max(0.1, score)

def evaluate_factual_accuracy(response: str, context: str) -> float:
    """
    Evaluate if the response aligns with the provided context
    Returns a score between 0 and 1
    """
    if not context:
        return 0.5  # Neutral score if no context provided

    context_lower = context.lower()
    response_lower = response.lower()

    # Count how many context phrases appear in the response
    context_sentences = context.split('.')
    matching_sentences = 0

    for sentence in context_sentences:
        if len(sentence.strip()) > 10:  # Only consider meaningful sentences
            if sentence.lower().strip() in response_lower:
                matching_sentences += 1

    if len(context_sentences) > 0:
        return min(1.0, (matching_sentences / len([s for s in context_sentences if len(s.strip()) > 10])) * 2)
    else:
        return 0.5

def run_answer_correctness_evaluation():
    """Run the answer correctness evaluation tests"""
    print("Starting LLM Answer Correctness Evaluation")
    print("=" * 60)

    results = []
    total_score = 0
    test_count = len(TEST_CASES)

    for i, test_case in enumerate(TEST_CASES):
        print(f"\nTest {i+1}: {test_case['question']}")

        # Get response from the LLM
        prompt = f"Context: {test_case['context']}\n\nQuestion: {test_case['question']}\n\nPlease provide a helpful and accurate response based only on the provided context."
        response = get_chatbot_response(prompt)

        print(f"Response: {response[:200]}...")

        # Evaluate the response
        relevance_score = evaluate_response_relevance(response, test_case['expected_topics'])
        coherence_score = evaluate_response_coherence(response)
        accuracy_score = evaluate_factual_accuracy(response, test_case['context'])

        # Calculate weighted average
        final_score = (relevance_score * 0.5) + (coherence_score * 0.3) + (accuracy_score * 0.2)

        result = {
            "question": test_case["question"],
            "response": response,
            "relevance_score": relevance_score,
            "coherence_score": coherence_score,
            "accuracy_score": accuracy_score,
            "final_score": final_score
        }

        results.append(result)
        total_score += final_score

        print(f"  Relevance Score: {relevance_score:.2f}")
        print(f"  Coherence Score: {coherence_score:.2f}")
        print(f"  Accuracy Score: {accuracy_score:.2f}")
        print(f"  Final Score: {final_score:.2f}")

    # Calculate overall metrics
    average_score = total_score / test_count if test_count > 0 else 0

    print("\n" + "=" * 60)
    print("LLM Answer Correctness Evaluation Results:")
    print(f"Total Tests: {test_count}")
    print(f"Average Score: {average_score:.2f}")

    # Performance thresholds
    if average_score >= 0.7:
        print("✓ Overall answer quality is good")
    elif average_score >= 0.5:
        print("⚠ Overall answer quality is acceptable but could be improved")
    else:
        print("✗ Overall answer quality needs significant improvement")

    # Detailed results
    print("\nDetailed Results:")
    for i, result in enumerate(results):
        status = "✓" if result["final_score"] >= 0.7 else "⚠"
        print(f"  {status} Test {i+1}: {result['final_score']:.2f} - {result['question'][:50]}...")

    # Return results for further analysis if needed
    return {
        "average_score": average_score,
        "results": results,
        "summary": {
            "total_tests": test_count,
            "passed": sum(1 for r in results if r["final_score"] >= 0.7),
            "failed": sum(1 for r in results if r["final_score"] < 0.7)
        }
    }

def run_comprehensive_evaluation():
    """Run a more comprehensive evaluation including edge cases"""
    print("\nRunning Comprehensive Evaluation with Edge Cases...")

    edge_cases = [
        {
            "question": "What is 2+2?",
            "expected_topics": ["4", "math", "addition"],
            "context": "Simple arithmetic question."
        },
        {
            "question": "Tell me about AI safety",
            "expected_topics": ["AI", "safety", "alignment", "ethics"],
            "context": "AI safety is an important field focusing on ensuring AI systems behave as intended."
        }
    ]

    edge_case_results = []

    for i, case in enumerate(edge_cases):
        print(f"\nEdge Case {i+1}: {case['question']}")

        prompt = f"Context: {case['context']}\n\nQuestion: {case['question']}\n\nProvide a concise, accurate response."
        response = get_chatbot_response(prompt)

        relevance_score = evaluate_response_relevance(response, case['expected_topics'])
        coherence_score = evaluate_response_coherence(response)

        print(f"  Response: {response[:150]}...")
        print(f"  Relevance: {relevance_score:.2f}")
        print(f"  Coherence: {coherence_score:.2f}")

        edge_case_results.append({
            "question": case["question"],
            "response": response,
            "relevance_score": relevance_score,
            "coherence_score": coherence_score
        })

    return edge_case_results

if __name__ == "__main__":
    # Run the main evaluation
    main_results = run_answer_correctness_evaluation()

    # Run additional edge case evaluation
    edge_results = run_comprehensive_evaluation()

    print(f"\n{'='*60}")
    print("Complete Evaluation Summary:")
    print(f"Main Tests Average Score: {main_results['average_score']:.2f}")
    print(f"Passed: {main_results['summary']['passed']}")
    print(f"Failed: {main_results['summary']['failed']}")
    print(f"Total: {main_results['summary']['total_tests']}")

    # Save results to file
    with open("llm_evaluation_results.json", "w") as f:
        json.dump({
            "main_results": main_results,
            "edge_case_results": edge_results
        }, f, indent=2)

    print("\nResults saved to llm_evaluation_results.json")