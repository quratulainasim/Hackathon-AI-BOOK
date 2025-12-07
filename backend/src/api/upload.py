import os
import uuid
import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from ..utils.document_processor import chunk_document, generate_file_hash
from ..utils.embedding_generator import generate_embedding
from ..services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME
from ..services.neon_db_client import insert_document_metadata, insert_chunk_metadata, init_db
from ..models.document_metadata import DocumentMetadata

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        init_db() # Ensure tables exist

        content = await file.read()
        file_content_str = content.decode("utf-8")
        content_hash = generate_file_hash(content)

        document_id = uuid.uuid4()
        filepath = os.path.join("uploaded_documents", file.filename) # Placeholder for actual storage path

        # 1. Chunk the document
        chunks = chunk_document(file_content_str, document_id)
        chunk_ids = [chunk.id for chunk in chunks]

        # 2. Generate embeddings and upload to Qdrant
        qdrant_points = []
        for chunk in chunks:
            embedding = generate_embedding(chunk.text_content)
            qdrant_points.append({
                "id": str(chunk.id),
                "payload": {
                    "document_id": str(chunk.document_id),
                    "text_content": chunk.text_content,
                    "page_number": chunk.page_number,
                    "order_in_document": chunk.order_in_document,
                },
                "vector": embedding
            })
            insert_chunk_metadata(chunk) # Store chunk metadata in Neon DB

        qdrant_client = get_qdrant_client()
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=qdrant_points
        )

        # 3. Store document metadata in Neon Postgres
        doc_metadata = DocumentMetadata(
            id=document_id,
            filename=file.filename,
            filepath=filepath,
            upload_date=datetime.datetime.now(),
            content_hash=content_hash,
            chunk_ids=chunk_ids
        )
        insert_document_metadata(doc_metadata)

        return {"message": "Document uploaded and processed successfully", "document_id": str(document_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {e}")
