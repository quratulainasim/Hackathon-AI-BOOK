"""
Script to process documentation files and add them to Qdrant vector database
"""

import os
import sys
import uuid
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.utils.document_processor import chunk_document, generate_file_hash
from backend.src.utils.embedding_generator import generate_embedding
from backend.src.services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME, ensure_collection_exists
from backend.src.services.neon_db_client import insert_document_metadata, insert_chunk_metadata, init_db
from backend.src.models.document_metadata import DocumentMetadata, ChunkMetadata
from datetime import datetime

def read_docs_directory(docs_path):
    """Read all markdown files from the docs directory"""
    doc_files = []
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                doc_files.append(os.path.join(root, file))
    return doc_files

def process_document_to_qdrant(file_path, doc_id):
    """Process a single document file and add to Qdrant"""
    print(f"Processing document: {file_path}")

    # Read the document content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate content hash
    content_hash = generate_file_hash(content.encode('utf-8'))

    # Chunk the document
    chunks = chunk_document(content, doc_id)
    chunk_ids = [chunk.id for chunk in chunks]

    # Generate embeddings and upload to Qdrant
    qdrant_client = get_qdrant_client()
    qdrant_points = []

    for chunk in chunks:
        try:
            embedding = generate_embedding(chunk.text_content)
            qdrant_points.append({
                "id": str(chunk.id),
                "payload": {
                    "document_id": str(chunk.document_id),
                    "text_content": chunk.text_content,
                    "page_number": chunk.page_number,
                    "order_in_document": chunk.order_in_document,
                    "source_file": file_path  # Track source file
                },
                "vector": embedding
            })
            # Store chunk metadata in Neon DB - try with string conversion
            try:
                insert_chunk_metadata(chunk)
            except Exception as chunk_db_error:
                print(f"  Warning: Could not store chunk metadata in DB: {chunk_db_error}")
                # Continue anyway since the vector is in Qdrant
            print(f"  Processed chunk {chunk.order_in_document + 1}")
        except Exception as e:
            print(f"  Error processing chunk: {e}")
            continue

    # Upload to Qdrant
    if qdrant_points:
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=qdrant_points
        )
        print(f"  Uploaded {len(qdrant_points)} chunks to Qdrant")

    # Store document metadata in Neon DB
    try:
        doc_metadata = DocumentMetadata(
            id=doc_id,
            filename=os.path.basename(file_path),
            filepath=file_path,
            upload_date=datetime.now(),  # Use current datetime
            content_hash=content_hash,
            chunk_ids=chunk_ids
        )
        insert_document_metadata(doc_metadata)
        print(f"  Document metadata stored in Neon DB")
    except Exception as doc_db_error:
        print(f"  Warning: Could not store document metadata in DB: {doc_db_error}")
        print(f"  However, {len(qdrant_points)} chunks were successfully added to Qdrant")

    return len(qdrant_points)

def main():
    print("Processing documentation files to Qdrant vector database...")

    # Initialize databases
    init_db()
    ensure_collection_exists()

    # Get all documentation files
    docs_path = os.path.join(os.path.dirname(__file__), 'docs')
    if not os.path.exists(docs_path):
        print(f"Docs directory not found: {docs_path}")
        return

    doc_files = read_docs_directory(docs_path)
    print(f"Found {len(doc_files)} documentation files")

    total_chunks = 0
    for file_path in doc_files:
        doc_id = uuid.uuid4()
        try:
            chunks_count = process_document_to_qdrant(file_path, doc_id)
            total_chunks += chunks_count
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    print(f"\nCompleted! Added {total_chunks} chunks from {len(doc_files)} documents to Qdrant.")
    print(f"Documents are now available for the RAG system to use as context.")

if __name__ == "__main__":
    main()