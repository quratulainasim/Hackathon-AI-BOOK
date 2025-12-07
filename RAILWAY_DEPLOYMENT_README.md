# AI-BOOK RAG Chatbot - Railway Deployment Guide

This guide explains how to deploy the AI-BOOK RAG Chatbot backend to Railway.

## Prerequisites

1. Railway account (sign up at [railway.app](https://railway.app))
2. GitHub account with your AI-BOOK repository
3. All required API keys and database URLs ready

## Environment Variables Required

Before deploying, ensure you have these environment variables ready:

- `GEMINI_API_KEY` - Your Google Gemini API key
- `QDRANT_URL` - Your Qdrant cloud instance URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `QDRANT_COLLECTION_NAME` - Your Qdrant collection name (default: "ai_book_chunks")
- `NEON_DB_URL` - Your Neon Postgres database connection string

## Deployment Methods

### Method 1: GitHub Integration (Recommended)

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your AI-BOOK repository
4. Railway will automatically detect the `Procfile` and deploy the application
5. Add the required environment variables in the "Variables" section of your project

### Method 2: Using Railway CLI

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Navigate to your project directory:
   ```bash
   cd e:/AI-BOOK
   ```

4. Link your project to Railway:
   ```bash
   railway link
   ```

5. Set environment variables:
   ```bash
   railway vars set GEMINI_API_KEY=your_gemini_api_key
   railway vars set QDRANT_URL=your_qdrant_url
   railway vars set QDRANT_API_KEY=your_qdrant_api_key
   railway vars set QDRANT_COLLECTION_NAME=your_collection_name
   railway vars set NEON_DB_URL=your_neon_db_url
   ```

6. Deploy:
   ```bash
   railway up
   ```

## File Structure for Railway

The deployment uses these key files:

- `Procfile` - Defines the start command for the application
- `runtime.txt` - Specifies the Python version to use
- `requirements.txt` - Lists all Python dependencies
- `railway.json` - Railway-specific configuration

## Backend Architecture

The backend is built with:
- **FastAPI** - Modern Python web framework
- **Qdrant** - Vector database for similarity search
- **Neon Postgres** - Metadata storage
- **Google Gemini** - LLM for response generation

## API Endpoints

Once deployed, your backend will be available at:
- `https://your-project-name-production.up.railway.app/health` - Health check
- `https://your-project-name-production.up.railway.app/ask` - Ask questions to the RAG system
- `https://your-project-name-production.up.railway.app/upload` - Upload documents
- `https://your-project-name-production.up.railway.app/documents` - List documents
- `https://your-project-name-production.up.railway.app/reindex` - Reindex documents

## Connecting Frontend to Backend

After deploying the backend, update your Docusaurus frontend to connect to the Railway backend:

1. In your Docusaurus project, update the API base URL:
   ```js
   // In ChatbotWidget.jsx and AdminPanel.jsx
   const API_BASE_URL = 'https://your-project-name-production.up.railway.app'; // Replace with your Railway URL
   ```

2. Rebuild and redeploy your Docusaurus site

## Troubleshooting

### Common Issues:

1. **Environment Variables Not Set**: Ensure all required environment variables are set in Railway
2. **Database Connection Issues**: Verify your Neon DB URL is properly formatted
3. **Qdrant Connection Issues**: Check that your Qdrant URL and API key are correct
4. **API Quota Limits**: Monitor your Google Gemini API usage

### Checking Logs:

You can view application logs in the Railway dashboard under the "Logs" tab for your project.

## Scaling

The application is designed to scale horizontally. As traffic increases, Railway can automatically scale your application instances.

## Monitoring

Monitor your:
- API usage for Google Gemini to avoid quota limits
- Qdrant vector database storage and query performance
- Database connection pool usage
- Application response times and error rates