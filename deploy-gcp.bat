@echo off
REM VayuDrishti GCP Deployment Script for Windows
REM This script deploys both backend and frontend to Google Cloud Platform

echo ========================================
echo VayuDrishti GCP Deployment
echo ========================================

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: gcloud CLI is not installed
    echo Install from: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

REM Set project ID
set PROJECT_ID=gee-data-490807
set REGION=us-central1

echo Setting GCP project to: %PROJECT_ID%
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo Enabling required GCP APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

REM Build and deploy using Cloud Build
echo Starting Cloud Build deployment...
gcloud builds submit --config=cloudbuild.yaml

echo ========================================
echo Deployment Complete!
echo ========================================

REM Get service URLs
echo.
echo Getting service URLs...
gcloud run services describe vayudrishti-backend --region=%REGION% --format="value(status.url)"
gcloud run services describe vayudrishti-frontend --region=%REGION% --format="value(status.url)"

echo.
echo Next Steps:
echo 1. Update frontend environment to use backend URL
echo 2. Test the application
echo 3. Configure custom domain if needed

pause
