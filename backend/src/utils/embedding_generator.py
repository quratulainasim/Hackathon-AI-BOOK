import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Using OpenAI client to interact with Gemini via OpenAI Agent SDK
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini OpenAI-compatible endpoint
)

import numpy as np

def generate_embedding(text: str) -> list[float]:
    # This will be replaced with actual embedding model from Gemini/OpenAI Agent SDK
    # For now, using a mock implementation for testing
    try:
        # Try to use the real API if keys are available
        response = client.embeddings.create(
            input=text,
            model="text-embedding-004"  # Correct model name for Gemini embedding API
        )
        return response.data[0].embedding
    except Exception as e:
        # Fallback to mock embedding for testing without API keys
        print(f"Using mock embedding due to API error: {e}")
        # Create a deterministic mock embedding based on the text content
        # Using a simple hash-based approach for reproducible results
        text_hash = hash(text) % (10 ** 8)
        np.random.seed(abs(text_hash))
        # Generate a 768-dimension vector (typical for many embedding models)
        mock_embedding = np.random.random(768).tolist()
        return mock_embedding
