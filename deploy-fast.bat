@echo off
echo ========================================
echo FAST BACKEND DEPLOYMENT TO GCP
echo ========================================
echo.

cd backend

echo [1/3] Building and deploying backend...
gcloud builds submit --config=../cloudbuild-fast.yaml --project=gee-data-490807

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo DEPLOYMENT SUCCESSFUL!
    echo ========================================
    echo.
    echo Backend URL: https://vayudrishti-backend-[hash].run.app
    echo.
    echo To get the exact URL, run:
    echo gcloud run services describe vayudrishti-backend --region=us-central1 --format="value(status.url)"
    echo.
) else (
    echo.
    echo ========================================
    echo DEPLOYMENT FAILED!
    echo ========================================
    echo Check the error messages above.
)

cd ..
pause
