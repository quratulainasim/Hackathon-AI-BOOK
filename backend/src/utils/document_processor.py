import os
import hashlib
from typing import List
import uuid
from ..models.document_metadata import ChunkMetadata

def generate_file_hash(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest()

def chunk_document(document_content: str, document_id: uuid.UUID, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[ChunkMetadata]:
    # This is a basic chunking implementation. More sophisticated methods might use NLP tools.
    chunks = []
    start = 0
    order = 0
    while start < len(document_content):
        end = start + chunk_size
        chunk_text = document_content[start:end]
        chunk_id = uuid.uuid4()
        chunks.append(ChunkMetadata(
            id=chunk_id,
            document_id=document_id,
            text_content=chunk_text,
            page_number=None, # To be determined by actual document parsing
            order_in_document=order
        ))
        start += chunk_size - chunk_overlap
        order += 1
    return chunks
