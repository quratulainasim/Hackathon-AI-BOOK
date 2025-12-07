"""
Test script for Qdrant integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME
from src.utils.embedding_generator import generate_embedding
from src.services.neon_db_client import init_db
import uuid

def test_qdrant_connection():
    print("Testing Qdrant connection...")

    try:
        qdrant_client = get_qdrant_client()
        print("Qdrant client initialized successfully")

        # Test health check - using get_collections as a simple connectivity test
        collections = qdrant_client.get_collections()
        print(f"Qdrant collections: {collections}")

        # Test collection existence (create if not exists)
        collection_exists = qdrant_client.collection_exists(QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' exists: {collection_exists}")

        if not collection_exists:
            print(f"Creating collection '{QDRANT_COLLECTION_NAME}'...")
            # Create collection with appropriate vector size (768 for our mock embeddings)
            qdrant_client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config={"size": 768, "distance": "Cosine"}  # Standard for text embeddings
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully")
        else:
            print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists")
            # Check the vector size of existing collection and recreate if needed
            collection_info = qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
            if hasattr(collection_info.config.params, 'vectors'):
                expected_size = 768
                actual_size = collection_info.config.params.vectors.size
                if actual_size != expected_size:
                    print(f"Collection has wrong vector size ({actual_size}), recreating...")
                    qdrant_client.delete_collection(QDRANT_COLLECTION_NAME)
                    qdrant_client.create_collection(
                        collection_name=QDRANT_COLLECTION_NAME,
                        vectors_config={"size": expected_size, "distance": "Cosine"}
                    )
                    print(f"Collection '{QDRANT_COLLECTION_NAME}' recreated with correct vector size")

        return True

    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return False

def test_embedding_generation():
    print("\nTesting embedding generation...")

    try:
        test_text = "This is a test sentence for embedding generation."
        embedding = generate_embedding(test_text)

        print(f"Embedding generated successfully")
        print(f"Embedding length: {len(embedding)}")
        print(f"Sample values: {embedding[:5]}...")  # First 5 values

        return True

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return False

def test_qdrant_storage():
    print("\nTesting Qdrant storage operations...")

    try:
        qdrant_client = get_qdrant_client()

        # Generate test embedding
        test_text = "This is a test document chunk for storage testing."
        embedding = generate_embedding(test_text)

        # Create a test point
        point_id = str(uuid.uuid4())
        test_point = {
            "id": point_id,
            "payload": {
                "document_id": str(uuid.uuid4()),
                "text_content": test_text,
                "page_number": 1,
                "order_in_document": 0,
            },
            "vector": embedding
        }

        # Insert the point
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[test_point]
        )
        print(f"Point inserted successfully with ID: {point_id}")

        # Search for the point
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=embedding,
            limit=1,
        )

        if search_result:
            found_point = search_result[0]
            print(f"Point retrieved successfully: {found_point.id}")
            print(f"Payload: {found_point.payload}")
        else:
            print("No points retrieved in search")
            return False

        # Clean up: delete the test point
        qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=[point_id]
        )
        print(f"Test point cleaned up successfully")

        return True

    except Exception as e:
        print(f"Error in Qdrant storage test: {e}")
        return False

def run_qdrant_tests():
    print("Starting Qdrant Integration Tests")
    print("=" * 50)

    tests = [
        ("Connection Test", test_qdrant_connection),
        ("Embedding Generation", test_embedding_generation),
        ("Storage Operations", test_qdrant_storage)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("Qdrant Integration Test Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall Result: {'PASS' if all_passed else 'FAIL'}")

    return all_passed

if __name__ == "__main__":
    run_qdrant_tests()