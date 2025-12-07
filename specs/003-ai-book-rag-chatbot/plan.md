# Implementation Plan: AI-BOOK RAG Chatbot

**Branch**: `003-ai-book-rag-chatbot` | **Date**: 2025-12-06 | **Spec**: [specs/003-ai-book-rag-chatbot/spec.md](specs/003-ai-book-rag-chatbot/spec.md)
**Input**: Feature specification from `/specs/003-ai-book-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for the "AI-BOOK RAG Chatbot", a system that integrates a Retrieval Augmented Generation (RAG) chatbot into a Docusaurus book. The system will feature a FastAPI backend, Qdrant Cloud for vector embeddings, Neon Serverless Postgres for metadata and file storage, and utilize the OpenAI Agent SDK with Gemini 2.5 Flash as the main Large Language Model (LLM). The frontend will be a Docusaurus chat widget, allowing users to ask questions and restrict answers to highlighted text.

## Technical Context

**Language/Version**: Python 3.x (Backend), JavaScript/TypeScript (Frontend - Docusaurus/React)
**Primary Dependencies**: FastAPI, Qdrant client, psycopg2/SQLAlchemy, OpenAI Agent SDK, Docusaurus, React
**Storage**: Qdrant Cloud (vector embeddings), Neon Serverless Postgres (metadata, file storage)
**Testing**: Python (pytest for backend), Frontend (Jest/React Testing Library for Docusaurus components - NEEDS CLARIFICATION: specific Docusaurus testing framework)
**Target Platform**: Cloud deployment (Backend), Web browser (Frontend)
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: Users receive answers within 5 seconds, document processing within 30 seconds.
**Constraints**: Qdrant Cloud Free Tier, Neon Serverless Postgres Free Tier, Gemini 2.5 Flash API rate limits, Docusaurus extensibility.
**Scale/Scope**: Support for at least 100 book chapters/documents.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Technical Accuracy & Clarity**: All technical details must be accurate and clearly explained for a computer science audience. (PASS - Plan details technical components and their interactions clearly.)
- [ ] **Research & Citation Integrity**: Research must adhere to APA style, with >=50% peer-reviewed sources and 0% plagiarism. (N/A for plan - This principle is primarily relevant for the book content, not the implementation plan itself. No specific research is being conducted *for* this plan that requires citations.)
- [x] **Content Scope & Length**: Plan must align with the book modules and target 5,000–7,000 words. (PASS - The plan aligns with the goal of building a RAG chatbot for the book.)
- [x] **Docusaurus & Output Format**: Plan must ensure output aligns with Docusaurus v3 Markdown and sidebars.js navigation. (PASS - The plan explicitly mentions Docusaurus integration and Markdown files for the book content.)
- [x] **Deployment & Hosting**: Plan must consider GitHub Pages and Vercel deployment configurations. (PASS - The plan includes deployment considerations for both backend and frontend.)

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-book-rag-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI endpoints
│   ├── services/        # Business logic, RAG pipeline
│   ├── models/          # Pydantic models, DB schemas
│   └── utils/           # Helper functions (chunking, embedding)
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/      # React components for chatbot UI
│   ├── pages/           # Docusaurus pages (if needed for chatbot)
│   ├── theme/           # Docusaurus theme overrides
│   └── utils/           # Frontend utilities for API interaction
└── tests/
```

**Structure Decision**: Web application structure with a `backend/` for FastAPI and `frontend/` for Docusaurus.

## Phase-wise Roadmap

### Phase 0: Setup & Core Backend (Backend Foundation)

**Goal**: Establish the basic FastAPI backend, database connections, and health check.
**Milestones**:
*   FastAPI application initialized.
*   Neon Serverless Postgres connection established.
*   Basic API structure for health endpoint.
**Tasks**:
*   Initialize FastAPI project.
*   Configure environment variables for database connections (Neon, Qdrant).
*   Implement database schema in Neon Postgres for document metadata.
*   Implement `/health` API endpoint.
*   Set up Dockerfile for backend containerization.

### Phase 1: Document Ingestion & Storage (RAG Pipeline - Part 1)

**Goal**: Implement document processing (chunking, embedding) and storage in Qdrant and Neon.
**Milestones**:
*   Document chunking utility developed.
*   Embedding generation integrated (e.g., using OpenAI embeddings or a similar model compatible with OpenAI Agent SDK).
*   Qdrant Cloud connection and collection setup.
*   `/upload` endpoint functional for ingesting new documents.
**Tasks**:
*   Develop document loading and chunking utility (e.g., using LangChain Text Splitters).
*   Integrate embedding model (e.g., text-embedding-ada-002 if using OpenAI Agent SDK for embeddings) for generating vector representations of chunks.
*   Implement Qdrant client for vector storage and retrieval.
*   Implement `/upload` API endpoint: receive file, chunk, embed, store in Qdrant, save metadata in Neon Postgres.
*   Implement `/documents` API endpoint: list metadata of uploaded documents from Neon Postgres.
*   Implement `/delete/{id}` API endpoint: remove document from Neon Postgres and corresponding vectors from Qdrant.
*   Implement `/reindex` API endpoint: trigger full reprocessing of all documents from Neon Postgres into Qdrant.

### Phase 2: RAG Chatbot Logic (RAG Pipeline - Part 2)

**Goal**: Integrate Gemini 2.5 Flash via OpenAI Agent SDK and implement the core `/ask` endpoint logic.
**Milestones**:
*   Gemini 2.5 Flash model accessible via OpenAI Agent SDK.
*   Retrieval mechanism for relevant chunks from Qdrant based on user query.
*   Context merging logic (highlighted text + retrieved chunks).
*   `/ask` endpoint fully functional, returning answers from Gemini.
**Tasks**:
*   Set up OpenAI Agent SDK to interact with Gemini 2.5 Flash.
*   Implement query embedding for user questions.
*   Develop retrieval function to query Qdrant for top-k relevant document chunks.
*   Implement logic to prioritize and merge highlighted text from frontend with retrieved chunks for prompt construction.
*   Integrate Gemini 2.5 Flash call within the `/ask` endpoint, passing the augmented prompt.
*   Ensure Gemini 2.5 Flash is instructed to respond *only* based on the provided context.

### Phase 3: Frontend Integration & UI (Docusaurus Chat Widget)

**Goal**: Integrate the chatbot UI into the Docusaurus book and connect it to the backend API.
**Milestones**:
*   Docusaurus custom component for chat widget created.
*   Chat widget communicates with `/ask` endpoint.
*   Text highlighting functionality integrated into Docusaurus.
**Tasks**:
*   Create a Docusaurus custom React component for the chatbot UI.
*   Implement client-side logic to send user queries to the `/ask` endpoint and display responses.
*   Develop functionality to capture highlighted text from the Docusaurus content and send it with the query to the backend.
*   Integrate the chat widget into the Docusaurus theme or specific pages.
*   Implement a UI for document management (upload, list, delete, reindex) for administrative users (basic UI for testing purposes).

### Phase 4: Deployment & Final Testing

**Goal**: Deploy the backend and frontend, and conduct comprehensive testing and validation.
**Milestones**:
*   Backend deployed to a cloud platform (e.g., a serverless platform or a container service).
*   Frontend (Docusaurus) deployed (e.g., GitHub Pages, Vercel).
*   End-to-end testing complete.
*   Performance metrics validated.
**Tasks**:
*   Configure deployment for FastAPI backend (e.g., using Docker and a cloud provider's services).
*   Configure deployment for Docusaurus frontend.
*   Conduct end-to-end integration tests between frontend and backend.
*   Perform retrieval precision testing to ensure relevant chunks are retrieved.
*   Conduct latency testing for `/ask`, `/upload`, and `/reindex` endpoints against success criteria.
*   Evaluate answer correctness from Gemini 2.5 Flash with diverse queries and contexts.
*   Implement basic monitoring and logging for deployed services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
