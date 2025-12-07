"""
Retrieval Precision Testing for AI-BOOK RAG Chatbot
Tests to ensure relevant document chunks are retrieved from Qdrant
"""

import os
import sys
import uuid
from typing import List, Tuple
import numpy as np
from dotenv import load_dotenv

# Add the backend src directory to the path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from backend.src.services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME
from backend.src.services.embedding_generator import generate_embeddings
from backend.src.utils.document_processor import chunk_document

load_dotenv()

def calculate_similarity(vector1: List[float], vector2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)

def test_retrieval_precision():
    """Test retrieval precision by comparing query embeddings with stored chunks"""
    print("Starting retrieval precision testing...")

    qdrant_client = get_qdrant_client()

    # Define test queries and expected relevant content
    test_queries = [
        {
            "query": "What is artificial intelligence?",
            "expected_content": ["artificial intelligence", "AI", "machine learning"]
        },
        {
            "query": "How does the RAG system work?",
            "expected_content": ["RAG", "retrieval", "augmented generation"]
        },
        {
            "query": "Explain neural networks",
            "expected_content": ["neural networks", "deep learning", "artificial intelligence"]
        }
    ]

    total_precision = 0.0
    total_recall = 0.0
    test_count = len(test_queries)

    for i, test_query in enumerate(test_queries):
        print(f"\nTest {i+1}: Query: '{test_query['query']}'")

        # Generate embedding for the query
        query_embedding = generate_embeddings([test_query["query"]])[0]

        # Search in Qdrant for similar chunks
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=10,  # Retrieve top 10 results
        )

        # Calculate precision and recall
        relevant_retrieved = 0
        total_relevant = 0

        for result in search_results:
            chunk_text = result.payload.get("text", "")
            is_relevant = any(expected.lower() in chunk_text.lower()
                            for expected in test_query["expected_content"])

            if is_relevant:
                relevant_retrieved += 1

        # For this test, we assume all chunks containing expected content are relevant
        # In a real scenario, you'd have a more sophisticated relevance assessment
        total_relevant = len(search_results)  # This is a simplified calculation

        precision = relevant_retrieved / len(search_results) if search_results else 0
        recall = relevant_retrieved / len(test_query["expected_content"]) if test_query["expected_content"] else 0

        print(f"  Retrieved {len(search_results)} chunks")
        print(f"  Relevant chunks retrieved: {relevant_retrieved}")
        print(f"  Precision: {precision:.2f}")
        print(f"  Recall: {recall:.2f}")

        total_precision += precision
        total_recall += recall

    avg_precision = total_precision / test_count
    avg_recall = total_recall / test_count

    print(f"\nAverage Precision: {avg_precision:.2f}")
    print(f"Average Recall: {avg_recall:.2f}")

    # Define acceptable thresholds
    precision_threshold = 0.7
    recall_threshold = 0.6

    print(f"\nPrecision Threshold: {precision_threshold}")
    print(f"Recall Threshold: {recall_threshold}")

    if avg_precision >= precision_threshold:
        print("✓ Retrieval precision meets threshold")
    else:
        print("⚠ Retrieval precision below threshold")

    if avg_recall >= recall_threshold:
        print("✓ Retrieval recall meets threshold")
    else:
        print("⚠ Retrieval recall below threshold")

    return avg_precision, avg_recall

def test_embedding_quality():
    """Test the quality of generated embeddings"""
    print("\nTesting embedding quality...")

    # Test with semantically similar sentences
    similar_sentences = [
        "What is artificial intelligence?",
        "How does AI work?",
        "Explain artificial intelligence",
        "What is machine learning?",
        "How does ML function?"
    ]

    embeddings = generate_embeddings(similar_sentences)

    # Calculate similarities between semantically similar sentences
    similarities = []
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim = calculate_similarity(embeddings[i], embeddings[j])
            similarities.append(sim)
            print(f"Similarity between '{similar_sentences[i]}' and '{similar_sentences[j]}': {sim:.3f}")

    avg_similarity = sum(similarities) / len(similarities) if similarities else 0
    print(f"Average similarity for semantically similar sentences: {avg_similarity:.3f}")

    # Test with dissimilar sentences
    dissimilar_sentences = [
        "What is artificial intelligence?",
        "How to bake a cake?",
        "Explain quantum physics",
        "What is the weather today?"
    ]

    dissimilar_embeddings = generate_embeddings(dissimilar_sentences)

    dissimilar_similarities = []
    for i in range(len(dissimilar_embeddings)):
        for j in range(i+1, len(dissimilar_embeddings)):
            sim = calculate_similarity(dissimilar_embeddings[i], dissimilar_embeddings[j])
            dissimilar_similarities.append(sim)

    avg_dissimilarity = sum(dissimilar_similarities) / len(dissimilar_similarities) if dissimilar_similarities else 0
    print(f"Average similarity for dissimilar sentences: {avg_dissimilarity:.3f}")

    return avg_similarity, avg_dissimilarity

def run_retrieval_precision_tests():
    """Run all retrieval precision tests"""
    print("Starting Retrieval Precision Tests for AI-BOOK RAG Chatbot")
    print("=" * 60)

    try:
        # Test retrieval precision
        precision, recall = test_retrieval_precision()

        # Test embedding quality
        avg_sim, avg_dissim = test_embedding_quality()

        print("\n" + "=" * 60)
        print("Retrieval Precision Test Results:")
        print(f"Average Precision: {precision:.2f}")
        print(f"Average Recall: {recall:.2f}")
        print(f"Average Similarity for Similar Sentences: {avg_sim:.3f}")
        print(f"Average Similarity for Dissimilar Sentences: {avg_dissim:.3f}")

        # Summary evaluation
        if precision >= 0.7 and recall >= 0.6:
            print("\n✓ Retrieval system performance is acceptable")
        else:
            print("\n⚠ Retrieval system performance needs improvement")

        if avg_sim > avg_dissim:
            print("✓ Embeddings distinguish between similar and dissimilar content")
        else:
            print("⚠ Embeddings may not effectively distinguish content")

        return True

    except Exception as e:
        print(f"Error during retrieval precision testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_retrieval_precision_tests()