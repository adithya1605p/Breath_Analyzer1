@echo off
echo ========================================
echo VayuDrishti - Simple GCP Deployment
echo ========================================
echo.

REM Check gcloud
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: gcloud not found!
    echo Install from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

echo Step 1: Setting project...
gcloud config set project gee-data-490807

echo.
echo Step 2: Enabling APIs...
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

echo.
echo Step 3: Deploying with Cloud Build...
echo This will take 10-15 minutes...
gcloud builds submit --config=cloudbuild.yaml

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Getting your URLs...
echo.

for /f "delims=" %%i in ('gcloud run services describe vayudrishti-backend --region us-central1 --format "value(status.url)"') do set BACKEND_URL=%%i
for /f "delims=" %%i in ('gcloud run services describe vayudrishti-frontend --region us-central1 --format "value(status.url)"') do set FRONTEND_URL=%%i

echo Backend:  %BACKEND_URL%
echo Frontend: %FRONTEND_URL%
echo.
echo Open your app: %FRONTEND_URL%
echo.

pause
