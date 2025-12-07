from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..services.llm_client import get_chatbot_response
from ..services.rag_pipeline import get_rag_response

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    highlighted_content: Optional[str] = None
    user_provided_text: Optional[str] = None  # Allow users to provide their own text for summarization

@router.post("/ask")
async def ask_chatbot(request: AskRequest):
    try:
        # If user provided text for summarization, use it directly
        if request.user_provided_text:
            # Create a specific prompt for text summarization
            summary_prompt = f"Please summarize the following text:\n\n{request.user_provided_text}\n\nSummary:"
            llm_answer = get_chatbot_response(summary_prompt)
        else:
            # The rag_response here is actually the constructed prompt based on RAG
            # This prompt is then passed to the LLM client
            rag_prompt = get_rag_response(
                user_question=request.question,
                highlighted_content=request.highlighted_content
            )
            llm_answer = get_chatbot_response(rag_prompt)

        return {"response": llm_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
