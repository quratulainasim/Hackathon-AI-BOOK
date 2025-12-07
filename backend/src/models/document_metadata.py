import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    id: uuid.UUID
    filename: str
    filepath: str
    upload_date: datetime.datetime
    content_hash: str
    chunk_ids: List[uuid.UUID]

class ChunkMetadata(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    text_content: str
    page_number: Optional[int]
    order_in_document: int
