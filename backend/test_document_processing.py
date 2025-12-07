"""
Test script for document processing and chunking functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.document_processor import chunk_document
import uuid

def test_chunking():
    print("Testing document chunking functionality...")

    # Create a test document
    test_document = """
    This is a test document for the AI-BOOK RAG Chatbot.

    The purpose of this document is to test the chunking functionality.

    The document contains multiple paragraphs to ensure that the chunking
    works properly with different types of content.

    Artificial intelligence (AI) is intelligence demonstrated by machines,
    in contrast to the natural intelligence displayed by animals including humans.
    Leading AI textbooks define the field as the study of "intelligent agents".

    Machine learning is a method of data analysis that automates analytical model building.
    It is a branch of artificial intelligence based on the idea that systems can learn
    from data, identify patterns and make decisions with minimal human intervention.

    Natural language processing (NLP) is a subfield of linguistics, computer science,
    and artificial intelligence concerned with the interactions between computers and human language.

    Deep learning is part of a broader family of machine learning methods based on
    artificial neural networks with representation learning.
    """

    # Generate a document ID
    doc_id = uuid.uuid4()

    # Test chunking
    chunks = chunk_document(test_document, doc_id, chunk_size=200, chunk_overlap=50)

    print(f"Original document length: {len(test_document)} characters")
    print(f"Number of chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} (ID: {chunk.id}):")
        print(f"Length: {len(chunk.text_content)} characters")
        print(f"Content preview: {chunk.text_content[:100]}...")
        print(f"Order: {chunk.order_in_document}")

    # Check for overlap
    if len(chunks) > 1:
        print(f"\nOverlap check:")
        for i in range(len(chunks) - 1):
            current_end = chunks[i].text_content[-50:]  # Last 50 chars of current chunk
            next_start = chunks[i+1].text_content[:50]   # First 50 chars of next chunk
            overlap = set(current_end) & set(next_start)
            print(f"Overlap between chunk {i+1} and {i+2}: {'Yes' if overlap else 'No'}")

    print("\nDocument chunking test completed successfully")

if __name__ == "__main__":
    test_chunking()