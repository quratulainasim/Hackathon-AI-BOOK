
import logging
import sys
import os

# Add the backend directory to the Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api import health, ask, upload, reindex, documents
from src.utils.logging_config import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up AI-BOOK RAG Chatbot Backend")
    yield
    # Shutdown
    logger.info("Shutting down AI-BOOK RAG Chatbot Backend")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from the frontend
# For production, replace "*" with your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware for logging requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

app.include_router(health.router)
app.include_router(ask.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(reindex.router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "AI-BOOK RAG Chatbot Backend", "status": "running"}
