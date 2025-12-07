import os
import psycopg2
from dotenv import load_dotenv
from ..models.document_metadata import DocumentMetadata, ChunkMetadata
import uuid
import datetime
from typing import List, Optional

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id UUID PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            filepath VARCHAR(255) NOT NULL,
            upload_date TIMESTAMP NOT NULL,
            content_hash VARCHAR(255) NOT NULL,
            chunk_ids UUID[]
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id UUID PRIMARY KEY,
            document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            text_content TEXT NOT NULL,
            page_number INTEGER,
            order_in_document INTEGER NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_document_metadata(doc_metadata: DocumentMetadata):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (id, filename, filepath, upload_date, content_hash, chunk_ids) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            doc_metadata.id,
            doc_metadata.filename,
            doc_metadata.filepath,
            doc_metadata.upload_date,
            doc_metadata.content_hash,
            [str(uid) for uid in doc_metadata.chunk_ids],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_document_metadata(doc_id: uuid.UUID) -> Optional[DocumentMetadata]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, filename, filepath, upload_date, content_hash, chunk_ids FROM documents WHERE id = %s", (str(doc_id),))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return DocumentMetadata(
            id=row[0],
            filename=row[1],
            filepath=row[2],
            upload_date=row[3],
            content_hash=row[4],
            chunk_ids=[uuid.UUID(uid) for uid in row[5]],
        )
    return None

def get_all_document_metadata() -> List[DocumentMetadata]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, filename, filepath, upload_date, content_hash, chunk_ids FROM documents")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        DocumentMetadata(
            id=row[0],
            filename=row[1],
            filepath=row[2],
            upload_date=row[3],
            content_hash=row[4],
            chunk_ids=[uuid.UUID(uid) for uid in row[5]],
        )
        for row in rows
    ]

def delete_document_metadata(doc_id: uuid.UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE id = %s", (str(doc_id),))
    conn.commit()
    cur.close()
    conn.close()

def insert_chunk_metadata(chunk_metadata: ChunkMetadata):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chunks (id, document_id, text_content, page_number, order_in_document) VALUES (%s, %s, %s, %s, %s)",
        (
            chunk_metadata.id,
            chunk_metadata.document_id,
            chunk_metadata.text_content,
            chunk_metadata.page_number,
            chunk_metadata.order_in_document,
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

def get_chunk_metadata(chunk_id: uuid.UUID) -> Optional[ChunkMetadata]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, document_id, text_content, page_number, order_in_document FROM chunks WHERE id = %s", (str(chunk_id),))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return ChunkMetadata(
            id=row[0],
            document_id=row[1],
            text_content=row[2],
            page_number=row[3],
            order_in_document=row[4],
        )
    return None
