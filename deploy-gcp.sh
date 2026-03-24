#!/bin/bash

# VayuDrishti GCP Deployment Script
# This script deploys both backend and frontend to Google Cloud Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}VayuDrishti GCP Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project ID
PROJECT_ID="gee-data-490807"
REGION="us-central1"

echo -e "${YELLOW}Setting GCP project to: $PROJECT_ID${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}Enabling required GCP APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo -e "${YELLOW}Starting Cloud Build deployment...${NC}"
gcloud builds submit --config=cloudbuild.yaml

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

# Get service URLs
BACKEND_URL=$(gcloud run services describe vayudrishti-backend --region=$REGION --format='value(status.url)')
FRONTEND_URL=$(gcloud run services describe vayudrishti-frontend --region=$REGION --format='value(status.url)')

echo -e "${GREEN}Backend URL:${NC} $BACKEND_URL"
echo -e "${GREEN}Frontend URL:${NC} $FRONTEND_URL"

echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Update frontend environment to use backend URL: $BACKEND_URL"
echo "2. Test the application at: $FRONTEND_URL"
echo "3. Configure custom domain if needed"
