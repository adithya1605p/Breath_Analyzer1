#!/bin/bash

# Deploy VayuDrishti Backend to GCP Cloud Run
# This script deploys ONLY the backend for faster deployment

PROJECT_ID="gee-data-490807"
REGION="us-central1"
SERVICE_NAME="vayudrishti-backend"

echo "🚀 Deploying VayuDrishti Backend to GCP Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Deploy directly from source (Cloud Run will build the Docker image)
echo "📦 Deploying backend from source..."
gcloud run deploy $SERVICE_NAME \
  --source backend \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars "WAQI_TOKEN=9abbe99f4595fa8a4d20dd26a06db8e375273034,GCP_PROJECT_ID=gee-data-490807,GCP_LOCATION=us-central1,SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co,SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY,VITE_SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co,VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY"

# Get the service URL
echo ""
echo "✅ Deployment complete!"
echo ""
BACKEND_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "🌐 Backend URL: $BACKEND_URL"
echo ""
echo "Test it:"
echo "curl $BACKEND_URL/health"
echo ""
echo "Update your Vercel frontend with:"
echo "VITE_API_URL=$BACKEND_URL"
