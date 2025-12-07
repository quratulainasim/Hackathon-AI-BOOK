# AI-BOOK RAG Chatbot - Complete Deployment Package

This package contains everything needed to deploy the AI-BOOK RAG Chatbot backend on Railway.

## Directory Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── Procfile                # Railway process file
├── runtime.txt             # Python version specification
├── railway.toml            # Railway configuration
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
└── src/                   # Source code directory
    ├── api/               # API route definitions
    ├── services/          # Business logic services
    ├── utils/             # Utility functions
    └── models/            # Data models
```

## Environment Variables Required

Create these environment variables in your Railway project:

```
GEMINI_API_KEY=your_google_gemini_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=your_collection_name
NEON_DB_URL=your_neon_database_connection_string
```

## Deployment Steps

### 1. Create Railway Account
- Go to https://railway.app
- Sign up using your GitHub account

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your AI-BOOK repository

### 3. Configure Variables
- Navigate to "Settings" → "Variables" in Railway
- Add all required environment variables listed above

### 4. Deploy
- Railway will automatically detect the Python application
- It will use the `Procfile` to start the application
- Monitor the deployment logs for any errors

### 5. Connect Frontend
Update your Docusaurus frontend to point to the Railway backend URL:

```js
// In your ChatbotWidget.jsx and AdminPanel.jsx
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://your-railway-app.up.railway.app';
```

## API Endpoints

Once deployed, your backend will be available at:
- `https://your-railway-app.up.railway.app/health` - Health check
- `https://your-railway-app.up.railway.app/ask` - Ask questions to the RAG system
- `https://your-railway-app.up.railway.app/upload` - Upload documents
- `https://your-railway-app.up.railway.app/documents` - List documents
- `https://your-railway-app.up.railway.app/reindex` - Reindex documents

## Scaling Considerations

- The application is designed to scale horizontally
- Qdrant and Neon DB handle the heavy lifting for vector storage and metadata
- Monitor your Google Gemini API usage to avoid quota limits

## Troubleshooting

Common issues and solutions:

1. **CORS Errors**: The backend allows all origins (`"*"`), but in production, specify your frontend domain

2. **API Quotas**: Google Gemini has usage limits; monitor your usage in the Google Cloud Console

3. **Database Connection**: Ensure your Neon DB connection string is properly formatted

4. **Qdrant Connection**: Verify your Qdrant cluster is accessible from Railway's network

## Maintenance

- Monitor application logs in Railway dashboard
- Keep dependencies updated
- Regularly backup your vector database and document metadata
- Monitor API usage and costs