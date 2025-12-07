import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

def get_qdrant_client():
    return qdrant_client

def ensure_collection_exists():
    """Ensure the Qdrant collection exists with the correct vector size"""
    collection_exists = qdrant_client.collection_exists(QDRANT_COLLECTION_NAME)
    if not collection_exists:
        # Create collection with appropriate vector size (768 for our embeddings)
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
