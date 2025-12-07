# Feature Specification: AI-BOOK RAG Chatbot

**Feature Branch**: `003-ai-book-rag-chatbot`
**Created**: 2025-12-06
**Status**: Draft
**Input**: User description: "You are an expert AI software architect. Specify the system requirements and technical specifications for a project called "AI-BOOK RAG Chatbot".

Requirements:
1. Build a RAG chatbot integrated into a Docusaurus book.
2. Use FastAPI as backend.
3. Use Qdrant Cloud Free Tier for vector embeddings.
4. Use Neon Serverless Postgres for metadata and file storage.
5. Use OpenAI Agent SDK with Gemini 2.5 Flash as the main LLM.
6. Allow users to highlight text; answers must be restricted to selected content if provided.
7. Implement chunking and embeddings for uploaded chapters or documents.
8. API endpoints: /ask, /upload, /documents, /delete/{id}, /reindex, /health.

Output:
- System components (Frontend, Backend, Databases, LLM)
- Tech stack
- Features list (functional & non-functional)
- Constraints, assumptions, and design choices
- Specify Gemini 2.5 Flash usage in the LLM pipeline"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question (Priority: P1)

As a Docusaurus book reader, I want to ask questions about the book content through a chatbot, so I can get instant answers without manually searching.

**Why this priority**: Core functionality, provides immediate value.

**Independent Test**: Can be tested by asking a question and verifying a relevant answer is returned.

**Acceptance Scenarios**:

1. **Given** the chatbot is integrated into the Docusaurus book, **When** I type a question in the chat interface, **Then** I receive a concise answer based on the book's content.
2. **Given** I highlight specific text in the book, **When** I ask a question, **Then** the answer is restricted to the highlighted content.

---

### User Story 2 - Upload New Content (Priority: P2)

As an administrator, I want to upload new chapters or documents, so the chatbot can index them and answer questions from the updated content.

**Why this priority**: Essential for content expansion and maintaining an up-to-date knowledge base.

**Independent Test**: Can be tested by uploading a new document and then asking a question specifically answerable by the new document.

**Acceptance Scenarios**:

1. **Given** I upload a new document, **When** the upload is complete, **Then** the document is chunked, embedded, and indexed for the chatbot.

---

### User Story 3 - Manage Documents (Priority: P3)

As an administrator, I want to view and delete uploaded documents, so I can manage the chatbot's knowledge base effectively.

**Why this priority**: Important for maintenance and data hygiene.

**Independent Test**: Can be tested by listing documents, deleting one, and verifying it no longer appears.

**Acceptance Scenarios**:

1. **Given** I request a list of documents, **When** the API responds, **Then** I receive a list of all uploaded document IDs and metadata.
2. **Given** I specify a document ID, **When** I request to delete it, **Then** the document is removed from the system.

---

### User Story 4 - Reindex Content (Priority: P3)

As an administrator, I want to trigger a reindex of all documents, so I can ensure the vector database is up-to-date and consistent.

**Why this priority**: For data consistency and recovery.

**Independent Test**: Can be tested by triggering reindex and verifying the system health.

**Acceptance Scenarios**:

1. **Given** I trigger a reindex, **When** the process completes, **Then** all documents are re-chunked and re-embedded into the vector database.

---

### User Story 5 - Check System Health (Priority: P4)

As a developer, I want to check the chatbot system's health, so I can monitor its operational status.

**Why this priority**: Basic operational monitoring.

**Independent Test**: Can be tested by querying the health endpoint and receiving a status.

**Acceptance Scenarios**:

1. **Given** I access the `/health` endpoint, **When** the system is operational, **Then** I receive a successful health status.

## Edge Cases

- What happens when a user asks a question that cannot be answered by the provided documents? The system should respond with a polite "I don't know" or indicate a lack of relevant information.
- How does the system handle very large document uploads? The system should implement appropriate chunking strategies and potentially async processing to handle large documents.
- What happens if Qdrant or Postgres services are unavailable? The system should implement graceful degradation, error logging, and retry mechanisms.
- What if the highlighted text is too short or irrelevant? The LLM should handle this gracefully, potentially ignoring the highlight if it's not useful and falling back to general RAG.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST integrate a RAG chatbot into a Docusaurus book.
- **FR-002**: Backend API MUST be built with FastAPI.
- **FR-003**: System MUST use Qdrant Cloud Free Tier for vector embeddings storage.
- **FR-004**: System MUST use Neon Serverless Postgres for metadata and file storage.
- **FR-005**: System MUST utilize OpenAI Agent SDK with Gemini 2.5 Flash as the main LLM for chat responses.
- **FR-006**: Users MUST be able to highlight text in the Docusaurus book.
- **FR-007**: Chatbot answers MUST be restricted to highlighted content if provided by the user.
- **FR-008**: System MUST implement chunking and embedding generation for uploaded chapters or documents.
- **FR-009**: Backend API MUST expose a `/ask` endpoint for chatbot queries.
- **FR-010**: Backend API MUST expose an `/upload` endpoint for uploading documents.
- **FR-011**: Backend API MUST expose a `/documents` endpoint to list uploaded documents.
- **FR-012**: Backend API MUST expose a `/delete/{id}` endpoint to delete a specific document.
- **FR-013**: Backend API MUST expose a `/reindex` endpoint to trigger re-chunking and re-embedding of all documents.
- **FR-014**: Backend API MUST expose a `/health` endpoint for system health checks.

### Key Entities

- **Document**: Represents an uploaded chapter or document. Attributes: `id` (UUID), `filename`, `filepath`, `upload_date`, `content_hash`, `chunk_ids` (list of references to chunks).
- **Chunk**: A small, semantically meaningful piece of a document. Attributes: `id` (UUID), `document_id`, `text_content`, `embedding_vector` (stored in Qdrant), `page_number` (optional), `order_in_document`.
- **User Query**: The question asked by the user. Attributes: `text`, `highlighted_content` (optional).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can ask questions about the book content and receive accurate, relevant answers within 5 seconds.
- **SC-002**: Uploaded documents are successfully processed (chunked, embedded, indexed) and available for querying within 30 seconds of upload.
- **SC-003**: The chatbot accurately restricts answers to highlighted text 95% of the time when highlighted text is provided.
- **SC-004**: All specified API endpoints are accessible and return appropriate responses with less than 2% error rate.
- **SC-005**: The system can store and retrieve at least 100 book chapters/documents efficiently with a consistent response time.

## Constraints, Assumptions, and Design Choices

### Constraints

- **Qdrant Cloud Free Tier**: Adherence to the limitations of Qdrant Cloud Free Tier regarding storage, collection size, and request rate.
- **Neon Serverless Postgres**: Adherence to the free tier limitations of Neon Serverless Postgres for database size and compute.
- **Docusaurus Integration**: Integration must work within the capabilities and extensibility points of Docusaurus v3.
- **Gemini 2.5 Flash API**: Usage must respect the API rate limits and token limits imposed by the Gemini 2.5 Flash model.

### Assumptions

- **Docusaurus UI Integration**: It is assumed that Docusaurus provides a suitable mechanism for integrating a custom chatbot UI widget or component into its frontend.
- **Document Format**: It is assumed that users will provide well-formed text-based documents (e.g., Markdown, PDF, TXT) for upload that are suitable for automatic chunking and embedding.
- **Content Suitability for RAG**: The book content is primarily text-based and conducive to effective Retrieval Augmented Generation.
- **Network Latency**: Assumed network latency to Qdrant Cloud, Neon Serverless Postgres, and Gemini 2.5 Flash API endpoints is within acceptable limits for responsive user experience.
- **User Authentication**: User authentication and authorization for admin-specific endpoints (`/upload`, `/documents`, `/delete/{id}`, `/reindex`) are considered out of scope for this initial specification, but will be a future enhancement.

### Design Choices

- **System Components**:
    -   **Frontend**: Docusaurus book with an integrated chatbot UI.
    -   **Backend**: FastAPI application.
    -   **Databases**: Qdrant Cloud (Vector DB), Neon Serverless Postgres (Metadata & File Storage).
    -   **LLM**: Gemini 2.5 Flash via OpenAI Agent SDK.
- **Tech Stack**:
    -   **Frontend**: Docusaurus v3, React (inherent to Docusaurus).
    -   **Backend**: Python 3.x, FastAPI, Pydantic, httpx (for API calls), Langchain or similar for RAG orchestration.
    -   **Vector Database**: Qdrant Cloud.
    -   **Relational Database**: Neon Serverless Postgres.
    -   **LLM Integration**: OpenAI Agent SDK.
- **Features List**:
    -   **Functional**:
        -   Chatbot interaction with book content.
        -   Contextual answers restricted by highlighted text.
        -   Document upload and indexing (chunking, embedding).
        -   Listing, deleting, and reindexing documents.
        -   System health check endpoint.
    -   **Non-functional**:
        -   Scalability (leveraging serverless databases).
        -   Responsiveness (target 5-second answer time).
        -   Data consistency.
        -   Modularity (Frontend/Backend separation).
- **LLM Pipeline with Gemini 2.5 Flash**:
    1.  **User Input**: The user interacts with the chatbot UI in the Docusaurus book, submitting a question. Optionally, the user can highlight a specific section of text within the book before asking a question.
    2.  **Context Augmentation (Retrieval)**:
        *   If highlighted text is provided by the user, this text is considered the primary and most relevant context. It is directly incorporated into the prompt.
        *   If no highlighted text is provided, the user's question is embedded into a vector representation. This vector is then used to perform a similarity search against the document chunks stored in Qdrant Cloud. The most semantically similar chunks are retrieved.
    3.  **Prompt Construction**: The retrieved chunks (if no highlight, or if highlight is too short/irrelevant and system decides to augment with more context) and/or the explicit highlighted text are combined with the user's original question. This forms a comprehensive and context-rich prompt.
    4.  **LLM Call**: The constructed prompt is sent to the Gemini 2.5 Flash model through the OpenAI Agent SDK. The OpenAI Agent SDK facilitates interaction with the Gemini API, ensuring proper formatting and handling of requests.
    5.  **Response Generation**: Gemini 2.5 Flash processes the prompt, utilizing the provided context to generate an accurate and relevant answer. A critical aspect is ensuring the LLM is instructed to answer *only* based on the provided context to minimize hallucinations.
    6.  **Output**: The generated answer from Gemini 2.5 Flash is returned through the FastAPI backend to the Docusaurus frontend, where it is displayed to the user in the chatbot interface.