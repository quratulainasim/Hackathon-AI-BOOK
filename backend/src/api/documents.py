from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from ..services.neon_db_client import get_all_document_metadata, delete_document_metadata
from ..services.qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME

router = APIRouter()

@router.get("/documents")
async def list_documents():
    try:
        documents = get_all_document_metadata()
        return [doc.dict() for doc in documents]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{document_id}")
async def delete_document(document_id: uuid.UUID):
    try:
        # Delete from Qdrant
        qdrant_client = get_qdrant_client()
        # Assuming chunks associated with document_id can be deleted via payload filter
        qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector={
                "filter": {
                    "must": [
                        {
                            "key": "document_id",
                            "match": {
                                "value": str(document_id)
                            }
                        }
                    ]
                }
            }
        )

        # Delete from Neon Postgres
        delete_document_metadata(document_id)

        return {"message": f"Document {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
