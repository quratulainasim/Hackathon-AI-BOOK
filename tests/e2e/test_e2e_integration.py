"""
End-to-End Integration Tests for AI-BOOK RAG Chatbot
Tests the integration between frontend and backend components
"""

import pytest
import requests
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"  # Update this to your backend URL
UPLOAD_FILE_PATH = "test_document.txt"

def create_test_document():
    """Create a test document for upload testing"""
    with open(UPLOAD_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write("""
        Test Document for AI-BOOK RAG Chatbot

        This is a sample document to test the RAG functionality.

        The AI-BOOK RAG Chatbot is designed to help users ask questions about AI, robotics, and related topics.

        Sample content for testing:
        - Document processing and chunking
        - Vector embedding generation
        - Similarity search in Qdrant
        - Context retrieval for LLM
        - Response generation with Gemini

        This document contains information about artificial intelligence, machine learning, and robotics.
        """)
    print(f"Created test document: {UPLOAD_FILE_PATH}")

def test_health_endpoint():
    """Test the health endpoint to ensure backend is running"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    print("✓ Health endpoint test passed")

def test_upload_document():
    """Test document upload functionality"""
    create_test_document()

    with open(UPLOAD_FILE_PATH, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "document_id" in data
    print(f"✓ Document upload test passed, document_id: {data['document_id']}")

    return data['document_id']

def test_list_documents():
    """Test listing uploaded documents"""
    response = requests.get(f"{BASE_URL}/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✓ Documents list test passed, found {len(data)} documents")

def test_ask_question():
    """Test asking a question to the RAG system"""
    # First, we need to have a document uploaded for context
    # For this test, we'll ask a general question that should work without specific context
    payload = {
        "question": "What is the AI-BOOK RAG Chatbot designed for?",
        "context": "The AI-BOOK RAG Chatbot is designed to help users ask questions about AI, robotics, and related topics."
    }

    response = requests.post(f"{BASE_URL}/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    print("✓ Ask question test passed")
    print(f"Response: {data['response'][:100]}...")

def test_delete_document(document_id):
    """Test deleting a document"""
    response = requests.delete(f"{BASE_URL}/delete/{document_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    print(f"✓ Document deletion test passed for document_id: {document_id}")

def test_reindex():
    """Test reindexing functionality"""
    response = requests.post(f"{BASE_URL}/reindex")
    # This might return 200 for success or 202 for accepted
    assert response.status_code in [200, 202]
    print("✓ Reindex test passed")

def run_all_e2e_tests():
    """Run all end-to-end integration tests"""
    print("Starting End-to-End Integration Tests...")

    # Wait a bit to ensure the backend is ready
    time.sleep(2)

    # Test 1: Health check
    test_health_endpoint()

    # Test 2: List documents (before upload)
    test_list_documents()

    # Test 3: Upload document
    doc_id = test_upload_document()

    # Test 4: List documents (after upload)
    test_list_documents()

    # Test 5: Ask a question
    test_ask_question()

    # Test 6: Reindex
    test_reindex()

    # Test 7: Delete document
    test_delete_document(doc_id)

    # Clean up test file
    if Path(UPLOAD_FILE_PATH).exists():
        Path(UPLOAD_FILE_PATH).unlink()

    print("\n✓ All End-to-End Integration Tests Passed!")

if __name__ == "__main__":
    run_all_e2e_tests()