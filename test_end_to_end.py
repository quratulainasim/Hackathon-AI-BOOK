"""
End-to-End Test for AI-BOOK RAG Chatbot
This script tests the complete functionality of the system
"""

import sys
import os
import time
import requests
from pathlib import Path

def test_backend_startup():
    """Test if backend can be imported without errors"""
    print("Testing backend startup...")
    try:
        # Add backend to path
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_path)

        from backend.main import app
        print("Backend imports successfully")
        return True
    except Exception as e:
        print(f"Backend import failed: {e}")
        return False

def test_document_processing():
    """Test document processing functionality"""
    print("\nTesting document processing...")
    try:
        from backend.src.utils.document_processor import chunk_document
        import uuid

        test_doc = "This is a test document to verify the chunking functionality of the AI-BOOK RAG Chatbot."
        doc_id = uuid.uuid4()
        chunks = chunk_document(test_doc, doc_id)

        print(f"Document chunked into {len(chunks)} chunks")
        return True
    except Exception as e:
        print(f"Document processing failed: {e}")
        return False

def test_embedding_generation():
    """Test embedding generation"""
    print("\nTesting embedding generation...")
    try:
        from backend.src.utils.embedding_generator import generate_embedding

        test_text = "Test embedding for end-to-end verification"
        embedding = generate_embedding(test_text)

        print(f"Generated embedding with {len(embedding)} dimensions")
        return True
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return False

def test_qdrant_integration():
    """Test Qdrant integration"""
    print("\nTesting Qdrant integration...")
    try:
        from backend.src.services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME, ensure_collection_exists

        # Ensure collection exists
        ensure_collection_exists()

        client = get_qdrant_client()
        collections = client.get_collections()

        print(f"Qdrant connection successful, collections: {[c.name for c in collections.collections]}")
        return True
    except Exception as e:
        print(f"Qdrant integration failed: {e}")
        return False

def test_llm_integration():
    """Test LLM integration"""
    print("\nTesting LLM integration...")
    try:
        from backend.src.services.llm_client import get_chatbot_response

        response = get_chatbot_response("Hello, this is a test message.")

        if response and len(response) > 0:
            print(f"LLM responded successfully")
            print(f"  Response preview: {response[:50]}...")
            return True
        else:
            print("LLM returned empty response")
            return False
    except Exception as e:
        print(f"LLM integration failed: {e}")
        return False

def test_rag_pipeline():
    """Test RAG pipeline"""
    print("\nTesting RAG pipeline...")
    try:
        from backend.src.services.rag_pipeline import get_rag_response

        response = get_rag_response("What is artificial intelligence?")

        if response and len(response) > 0:
            print(f"RAG pipeline responded successfully")
            print(f"  Response preview: {response[:50]}...")
            return True
        else:
            print("RAG pipeline returned empty response")
            return False
    except Exception as e:
        print(f"RAG pipeline failed: {e}")
        return False

def test_api_endpoints():
    """Test if API endpoints can be imported"""
    print("\nTesting API endpoints...")
    try:
        # Test that all API modules can be imported
        from backend.src.api import health, ask, upload, documents, reindex

        print("All API endpoints imported successfully")
        return True
    except Exception as e:
        print(f"API endpoints failed: {e}")
        return False

def test_frontend_components():
    """Test frontend components exist"""
    print("\nTesting frontend components...")
    try:
        # Check if frontend components exist in the correct location
        frontend_components = [
            "src/components/ChatbotWidget.jsx",
            "src/components/ChatbotWidget.css",
            "src/components/AdminPanel.jsx",
            "src/components/AdminPanel.css",
            "src/theme/Layout.js"
        ]

        all_exist = True
        for component in frontend_components:
            path = os.path.join(os.path.dirname(__file__), component)
            if not os.path.exists(path):
                print(f"Frontend component missing: {component}")
                all_exist = False
            else:
                print(f"Frontend component exists: {component}")

        return all_exist
    except Exception as e:
        print(f"Frontend components test failed: {e}")
        return False

def run_end_to_end_tests():
    """Run all end-to-end tests"""
    print("Starting End-to-End Tests for AI-BOOK RAG Chatbot")
    print("=" * 60)

    tests = [
        ("Backend Startup", test_backend_startup),
        ("Document Processing", test_document_processing),
        ("Embedding Generation", test_embedding_generation),
        ("Qdrant Integration", test_qdrant_integration),
        ("LLM Integration", test_llm_integration),
        ("RAG Pipeline", test_rag_pipeline),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Components", test_frontend_components),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 60)
    print("End-to-End Test Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall Result: {'PASS' if all_passed else 'FAIL'}")

    if all_passed:
        print("\nAll end-to-end tests passed! The AI-BOOK RAG Chatbot is ready for use.")
    else:
        print("\nSome tests failed. Please review the issues above.")

    return all_passed

if __name__ == "__main__":
    run_end_to_end_tests()