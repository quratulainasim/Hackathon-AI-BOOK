from typing import List, Optional
from .qdrant_client import get_qdrant_client, QDRANT_COLLECTION_NAME
from ..utils.embedding_generator import generate_embedding
from .neon_db_client import get_chunk_metadata
import uuid

def retrieve_relevant_chunks(query_embedding: List[float], limit: int = 5) -> List[str]:
    qdrant_client = get_qdrant_client()
    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit,
    )
    chunks = []
    for hit in search_result:
        # Directly get text content from the Qdrant payload since Neon DB had UUID issues
        if hasattr(hit, 'payload') and 'text_content' in hit.payload:
            chunks.append(hit.payload['text_content'])
        # Fallback to Neon DB if needed
        elif hasattr(hit, 'id'):
            chunk_id = uuid.UUID(hit.id)
            chunk_metadata = get_chunk_metadata(chunk_id)
            if chunk_metadata:
                chunks.append(chunk_metadata.text_content)
    return chunks

def construct_prompt(user_question: str, highlighted_content: Optional[str] = None, retrieved_chunks: Optional[List[str]] = None) -> str:
    context = ""
    if highlighted_content:
        context += f"User highlighted content: {highlighted_content}\n\n"

    if retrieved_chunks:
        context += "Retrieved document chunks:\n"
        for i, chunk in enumerate(retrieved_chunks):
            context += f"Chunk {i+1}: {chunk}\n"
        context += "\n"

    if context:
        prompt = f"Based on the following context, answer the user's question. If the answer is not available in the context, state that you don't know.\n\n{context}User question: {user_question}"
    else:
        prompt = f"Answer the following question. If the answer is not available in the context, state that you don't know.\n\nUser question: {user_question}"

    return prompt

def get_rag_response(user_question: str, highlighted_content: Optional[str] = None) -> str:
    retrieved_chunks = []
    if not highlighted_content:
        query_embedding = generate_embedding(user_question)
        retrieved_chunks = retrieve_relevant_chunks(query_embedding)

    prompt = construct_prompt(user_question, highlighted_content, retrieved_chunks)
    return prompt # This will be passed to the LLM client
