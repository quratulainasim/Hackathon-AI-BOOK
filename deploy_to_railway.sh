#!/bin/bash

# Deployment script for AI-BOOK RAG Chatbot Backend to Railway

echo "Preparing AI-BOOK RAG Chatbot for Railway deployment..."

# Create a deployment directory with only necessary backend files
mkdir -p deployment/backend/src/api
mkdir -p deployment/backend/src/services
mkdir -p deployment/backend/src/utils
mkdir -p deployment/backend/src/models

# Copy backend source files
cp -r backend/src/api/*.py deployment/backend/src/api/
cp -r backend/src/services/*.py deployment/backend/src/services/
cp -r backend/src/utils/*.py deployment/backend/src/utils/
cp -r backend/src/models/*.py deployment/backend/src/models/
cp backend/main.py deployment/backend/
cp backend/requirements.txt deployment/backend/
cp backend/Procfile deployment/backend/
cp backend/runtime.txt deployment/backend/

# Copy root deployment files
cp Procfile deployment/
cp runtime.txt deployment/
cp requirements.txt deployment/
cp railway.json deployment/

echo "Deployment package created in ./deployment/"
echo "To deploy to Railway:"
echo "1. Install Railway CLI: npm install -g @railway/cli"
echo "2. Login: railway login"
echo "3. Navigate to the deployment directory: cd deployment"
echo "4. Link to your Railway project: railway link"
echo "5. Deploy: railway up"
echo ""
echo "Alternatively, connect your GitHub repo to Railway through the dashboard."