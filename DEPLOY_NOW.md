# Deploy VayuDrishti to GCP - Quick Start

## 1. Install Google Cloud SDK

**Windows:**
Download and install from: https://cloud.google.com/sdk/docs/install

**Verify installation:**
```bash
gcloud --version
```

## 2. Login and Set Project

```bash
gcloud auth login
gcloud config set project gee-data-490807
```

## 3. Deploy (Choose One Method)

### Method A: Automated (Easiest)

**Windows:**
```bash
deploy-gcp.bat
```

**Linux/Mac:**
```bash
chmod +x deploy-gcp.sh
./deploy-gcp.sh
```

### Method B: Manual (Step by Step)

#### Enable APIs:
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
```

#### Deploy Backend:
```bash
cd backend
gcloud builds submit --tag gcr.io/gee-data-490807/vayudrishti-backend
gcloud run deploy vayudrishti-backend --image gcr.io/gee-data-490807/vayudrishti-backend --region us-central1 --platform managed --allow-unauthenticated --memory 2Gi --cpu 2
```

#### Get Backend URL:
```bash
gcloud run services describe vayudrishti-backend --region us-central1 --format 'value(status.url)'
```

#### Deploy Frontend:
```bash
cd ../web-frontend
# Update .env.production with backend URL first!
gcloud builds submit --tag gcr.io/gee-data-490807/vayudrishti-frontend
gcloud run deploy vayudrishti-frontend --image gcr.io/gee-data-490807/vayudrishti-frontend --region us-central1 --platform managed --allow-unauthenticated
```

## 4. Access Your App

After deployment completes, you'll get URLs like:
- Backend: `https://vayudrishti-backend-xxxxx-uc.a.run.app`
- Frontend: `https://vayudrishti-frontend-xxxxx-uc.a.run.app`

## 5. Update Frontend to Use Backend

If you deployed manually, update `web-frontend/.env.production`:
```env
VITE_API_URL=<YOUR_BACKEND_URL>
```

Then redeploy frontend.

## Troubleshooting

**"Permission denied":**
```bash
gcloud auth application-default login
```

**"Billing not enabled":**
Enable billing in GCP Console: https://console.cloud.google.com/billing

**"Service account error":**
```bash
gcloud iam service-accounts list
```

## Cost

- Backend: ~$60-80/month (with auto-scaling)
- Frontend: ~$15-20/month (with auto-scaling)
- Total: ~$75-100/month

With low traffic, costs will be much lower due to auto-scaling.

## Need Help?

See full guide: `GCP_DEPLOYMENT_GUIDE.md`
