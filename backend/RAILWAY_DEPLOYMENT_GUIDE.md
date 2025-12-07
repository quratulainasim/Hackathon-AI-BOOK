# Deploying AI-BOOK RAG Chatbot Backend on Railway

This guide explains how to deploy the FastAPI backend of the AI-BOOK RAG Chatbot on Railway.

## Prerequisites

1. Railway account (sign up at [railway.app](https://railway.app))
2. GitHub account (Railway integrates with GitHub)
3. All required API keys and database URLs

## Steps to Deploy

### 1. Prepare Your Repository

Make sure your repository contains:
- `requirements.txt` with all dependencies
- `Procfile` (created for Railway deployment)
- `runtime.txt` specifying Python version
- `railway.toml` configuration file
- All source code in the `src/` directory
- Proper environment variables in `.env.example`

### 2. Link Your GitHub Repository to Railway

1. Sign in to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your AI-BOOK repository

### 3. Configure Environment Variables

After linking your repository, go to the "Variables" section in Railway and add:

```
GEMINI_API_KEY=your_google_gemini_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=your_collection_name
NEON_DB_URL=your_neon_database_connection_string
```

### 4. Deploy the Application

1. In Railway, go to your project
2. Click "Deploy Now" or wait for automatic deployment if you enabled it
3. Monitor the deployment logs to ensure everything installs correctly

### 5. Access Your Deployed Backend

Once deployed, Railway will provide a URL for your backend in the format:
`https://your-project-name-production.up.railway.app`

## Connecting Frontend to Deployed Backend

After deployment, update your Docusaurus frontend to use the deployed backend:

1. In your Docusaurus project, update the environment variables or API endpoints to point to your Railway deployment
2. The chatbot widget will now connect to the live backend instead of localhost

## Important Notes

- The application will use the environment variables from Railway
- Make sure your Qdrant and Neon database connections are accessible from Railway
- Monitor your API usage to avoid exceeding quotas
- For production, consider restricting CORS origins to your specific frontend domain

## Troubleshooting

If you encounter issues:
1. Check the deployment logs in Railway for error messages
2. Verify all environment variables are correctly set
3. Confirm that your database and vector store are accessible from Railway
4. Check that the port binding uses the `$PORT` environment variable provided by Railway