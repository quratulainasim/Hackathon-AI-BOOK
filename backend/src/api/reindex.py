from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid

from ..services.neon_db_client import get_all_document_metadata, get_chunk_metadata, delete_document_metadata, insert_document_metadata, insert_chunk_metadata
from ..services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME
from ..utils.document_processor import chunk_document, generate_file_hash
from ..utils.embedding_generator import generate_embedding
from ..models.document_metadata import DocumentMetadata, ChunkMetadata

router = APIRouter()

async def reindex_documents_task():
    documents = get_all_document_metadata()
    qdrant_client = get_qdrant_client()

    for doc in documents:
        try:
            # For reindexing, we assume the original file content might be available or re-fetchable.
            # For this example, we'll simulate re-reading content based on stored metadata.
            # In a real scenario, you'd need access to the actual file content.
            # For simplicity, we'll just re-process based on existing chunk text.

            # Delete old chunks from Qdrant and Neon DB for this document
            qdrant_client.delete(
                collection_name=QDRANT_COLLECTION_NAME,
                points_selector={
                    "filter": {
                        "must": [
                            {
                                "key": "document_id",
                                "match": {
                                    "value": str(doc.id)
                                }
                            }
                        ]
                    }
                }
            )
            # In a real system, you'd also delete old chunk metadata from Neon DB

            # Simulate re-chunking and re-embedding (using existing text content from old chunks for demo)
            # In a real system, you'd load the full document content from storage (e.g., filepath) and re-chunk it.
            # For this example, we'll concatenate existing chunk texts to simulate original document for re-chunking.
            full_document_content = " ".join([get_chunk_metadata(chunk_id).text_content for chunk_id in doc.chunk_ids if get_chunk_metadata(chunk_id)])

            new_chunks = chunk_document(full_document_content, doc.id)
            new_chunk_ids = [chunk.id for chunk in new_chunks]

            new_qdrant_points = []
            for chunk in new_chunks:
                embedding = generate_embedding(chunk.text_content)
                new_qdrant_points.append({
                    "id": str(chunk.id),
                    "payload": {
                        "document_id": str(chunk.document_id),
                        "text_content": chunk.text_content,
                        "page_number": chunk.page_number,
                        "order_in_document": chunk.order_in_document,
                    },
                    "vector": embedding
                })
                insert_chunk_metadata(chunk) # Store new chunk metadata in Neon DB

            if new_qdrant_points:
                qdrant_client.upsert(
                    collection_name=QDRANT_COLLECTION_NAME,
                    points=new_qdrant_points
                )

            # Update document metadata with new chunk IDs
            doc.chunk_ids = new_chunk_ids
            # In a real system, you'd update the existing document entry, not re-insert
            delete_document_metadata(doc.id) # Delete old record
            insert_document_metadata(doc) # Insert updated record

        except Exception as e:
            print(f"Error reindexing document {doc.id}: {e}")

@router.post("/reindex")
async def reindex_all_documents(background_tasks: BackgroundTasks):
    background_tasks.add_task(reindex_documents_task)
    return {"message": "Reindexing initiated in the background"}
