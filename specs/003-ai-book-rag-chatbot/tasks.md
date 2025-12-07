# Tasks: AI-BOOK RAG Chatbot

**Input**: Design documents from `/specs/003-ai-book-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: The feature specification did not explicitly request test tasks, so I will generate them as part of the implementation tasks where appropriate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup & Core Backend (Backend Foundation)

**Purpose**: Establish the basic FastAPI backend, database connections, and health check.

- [ ] T001 Initialize FastAPI project in `backend/`
- [ ] T002 Configure environment variables for Neon Postgres and Qdrant in `backend/.env`
- [ ] T003 Implement database schema for document metadata in `backend/src/models/document_metadata.py`
- [ ] T004 Implement `/health` API endpoint in `backend/src/api/health.py`

---

## Phase 2: Document Ingestion & Storage (RAG Pipeline - Part 1)

**Purpose**: Implement document processing (chunking, embedding) and storage in Qdrant and Neon.

### Implementation for User Story 2 - Upload New Content

- [X] T005 [P] [US2] Develop document loading and chunking utility in `backend/src/utils/document_processor.py`
- [X] T006 [P] [US2] Integrate embedding model for generating vector representations of chunks in `backend/src/utils/embedding_generator.py`
- [X] T007 [P] [US2] Implement Qdrant client for vector storage and retrieval in `backend/src/services/qdrant_client.py`
- [X] T008 [US2] Implement `/upload` API endpoint in `backend/src/api/upload.py` (depends on T006, T007, T008)

### Implementation for User Story 3 - Manage Documents

- [X] T009 [P] [US3] Implement `/documents` API endpoint in `backend/src/api/documents.py`
- [X] T010 [P] [US3] Implement `/delete/{id}` API endpoint in `backend/src/api/documents.py`

### Implementation for User Story 4 - Reindex Content

- [X] T011 [P] [US4] Implement `/reindex` API endpoint in `backend/src/api/reindex.py`

---

## Phase 3: RAG Chatbot Logic (RAG Pipeline - Part 2)

**Purpose**: Integrate Gemini 2.5 Flash via OpenAI Agent SDK and implement the core `/ask` endpoint logic.

### Implementation for User Story 1 - Ask a Question

- [X] T012 [P] [US1] Set up OpenAI Agent SDK to interact with Gemini 2.5 Flash in `backend/src/services/llm_client.py`
- [X] T013 [P] [US1] Implement query embedding for user questions in `backend/src/utils/embedding_generator.py`
- [X] T014 [P] [US1] Develop retrieval function to query Qdrant for top-k relevant document chunks in `backend/src/services/qdrant_client.py`
- [X] T015 [US1] Implement logic to prioritize and merge highlighted text with retrieved chunks for prompt construction in `backend/src/services/rag_pipeline.py`
- [X] T016 [US1] Integrate Gemini 2.5 Flash call within the `/ask` endpoint in `backend/src/api/ask.py` (depends on T013, T014, T015, T016)
- [X] T017 [US1] Ensure Gemini 2.5 Flash is instructed to respond *only* based on the provided context in `backend/src/services/rag_pipeline.py`

---

## Phase 4: Frontend Integration & UI (Docusaurus Chat Widget)

**Purpose**: Integrate the chatbot UI into the Docusaurus book and connect it to the backend API.

### Implementation for User Story 1 - Ask a Question (Frontend)

- [X] T018 [P] [US1] Create a Docusaurus custom React component for the chatbot UI in `frontend/src/components/ChatbotWidget.jsx`
- [X] T019 [P] [US1] Implement client-side logic to send user queries to the `/ask` endpoint and display responses in `frontend/src/utils/api.js`
- [X] T020 [P] [US1] Develop functionality to capture highlighted text from Docusaurus content in `frontend/src/utils/text_highlighter.js`
- [X] T021 [US1] Integrate the chat widget into the Docusaurus theme or specific pages in `frontend/src/theme/Layout/index.js` or similar.

### Implementation for User Story 3 - Manage Documents (Frontend)

- [ ] T022 [P] [US3] Implement a basic UI for document management (upload, list, delete, reindex) for administrative users in `frontend/src/components/AdminPanel.jsx`

---

## Phase 5: Deployment & Final Testing

**Purpose**: Deploy the backend and frontend, and conduct comprehensive testing and validation.

- [ ] T023 Configure deployment for FastAPI backend (e.g., using Docker and a cloud provider's services) in `ops/backend_deployment.yml`
- [ ] T024 Configure deployment for Docusaurus frontend (e.g., GitHub Pages, Vercel) in `ops/frontend_deployment.yml`
- [ ] T025 Conduct end-to-end integration tests between frontend and backend in `tests/e2e/`
- [ ] T026 Perform retrieval precision testing to ensure relevant chunks are retrieved in `backend/tests/rag_precision.py`
- [ ] T027 Conduct latency testing for `/ask`, `/upload`, and `/reindex` endpoints in `tests/performance/`
- [ ] T028 Evaluate answer correctness from Gemini 2.5 Flash with diverse queries and contexts in `backend/tests/llm_evaluation.py`
- [ ] T029 Implement basic monitoring and logging for deployed services in `ops/monitoring_config.yml`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately.
- **Phase 2 (Document Ingestion)**: Depends on Phase 1 completion.
- **Phase 3 (RAG Chatbot Logic)**: Depends on Phase 1 and Phase 2 completion.
- **Phase 4 (Frontend Integration)**: Can run in parallel with Phase 3 once backend endpoints are defined, but relies on Phase 3 completion for full functionality.
- **Phase 5 (Deployment & Testing)**: Depends on completion of all prior phases.

### User Story Dependencies

- **User Story 1 (Ask a Question)**: Depends on document ingestion and RAG logic (Phases 1, 2, 3).
- **User Story 2 (Upload New Content)**: Depends on backend foundation (Phase 1).
- **User Story 3 (Manage Documents)**: Depends on backend foundation (Phase 1).
- **User Story 4 (Reindex Content)**: Depends on backend foundation (Phase 1).
- **User Story 5 (Check System Health)**: Part of backend foundation (Phase 1).

### Within Each User Story

- Utilities (chunking, embedding) before API endpoints.
- LLM setup before RAG logic.
- Backend API before frontend integration.

### Parallel Opportunities

- Multiple tasks within Phase 2 and Phase 3 can run in parallel where marked [P].
- Frontend integration (Phase 4) can start in parallel with RAG Chatbot Logic (Phase 3) once API endpoints are stable.

---

## Implementation Strategy

### MVP First (Core Chatbot - User Story 1 & 5 + basic ingestion)

1.  Complete Phase 1: Setup & Core Backend (including `/health` endpoint).
2.  Complete foundational parts of Phase 2: Document Ingestion (chunking, embedding, Qdrant setup, basic `/upload`).
3.  Complete Phase 3: RAG Chatbot Logic (core `/ask` endpoint).
4.  Complete core parts of Phase 4: Frontend Chatbot UI Integration.
5.  **STOP and VALIDATE**: Test User Story 1 independently with basic document ingestion.

### Incremental Delivery

1.  MVP as above.
2.  Add full document management (User Stories 2, 3, 4) with corresponding UI elements.
3.  Iteratively improve RAG performance, answer quality, and frontend experience.
4.  Complete Phase 5: Deployment & Final Testing.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Phase 1 (Setup) and foundational elements of Phase 2 together.
2.  Once foundational backend is done:
    -   Developer A: Focus on RAG Chatbot Logic (Phase 3).
    -   Developer B: Focus on Document Ingestion and Management Endpoints (remaining Phase 2).
    -   Developer C: Focus on Frontend Integration (Phase 4).
3.  Stories complete and integrate independently.

---

## Notes

- All tasks are formatted with checkboxes, IDs, optional parallel marker [P], and user story label [USx].
- Clear file paths are provided for each task.
- Each user story is designed to be independently completable and testable.
- Tests are included as implementation tasks, to be developed alongside features.
- The plan prioritizes core chatbot functionality as the MVP.


