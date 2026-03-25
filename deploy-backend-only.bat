@echo off
echo ========================================
echo BACKEND-ONLY DEPLOYMENT TO GCP
echo ========================================
echo.

cd backend

echo Building and deploying backend to Cloud Run...
echo This should take 3-5 minutes...
echo.

gcloud run deploy vayudrishti-backend ^
  --source . ^
  --region=us-central1 ^
  --platform=managed ^
  --allow-unauthenticated ^
  --memory=2Gi ^
  --cpu=2 ^
  --min-instances=1 ^
  --max-instances=10 ^
  --set-env-vars=WAQI_TOKEN=9abbe99f4595fa8a4d20dd26a06db8e375273034,GCP_PROJECT_ID=gee-data-490807,GCP_LOCATION=us-central1,SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co,SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY ^
  --project=gee-data-490807

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Getting your backend URL...
    gcloud run services describe vayudrishti-backend --region=us-central1 --format="value(status.url)" --project=gee-data-490807
    echo.
) else (
    echo.
    echo ========================================
    echo DEPLOYMENT FAILED!
    echo ========================================
)

cd ..
pause
