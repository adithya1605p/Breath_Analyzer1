# VayuDrishti - GCP Deployment Guide

## Prerequisites

1. **Google Cloud Account**
   - Active GCP account with billing enabled
   - Project ID: `gee-data-490807`

2. **Install Google Cloud SDK**
   - Download from: https://cloud.google.com/sdk/docs/install
   - Verify installation: `gcloud --version`

3. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project gee-data-490807
   ```

## Deployment Options

### Option 1: Automated Deployment (Recommended)

**Windows:**
```bash
deploy-gcp.bat
```

**Linux/Mac:**
```bash
chmod +x deploy-gcp.sh
./deploy-gcp.sh
```

This will:
- Enable required GCP APIs
- Build Docker images for backend and frontend
- Deploy to Cloud Run
- Display service URLs

### Option 2: Manual Deployment

#### Step 1: Enable APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### Step 2: Build and Deploy Backend
```bash
cd backend

# Build Docker image
gcloud builds submit --tag gcr.io/gee-data-490807/vayudrishti-backend

# Deploy to Cloud Run
gcloud run deploy vayudrishti-backend \
  --image gcr.io/gee-data-490807/vayudrishti-backend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars WAQI_TOKEN=9abbe99f4595fa8a4d20dd26a06db8e375273034,GCP_PROJECT_ID=gee-data-490807,GCP_LOCATION=us-central1,SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co,SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY
```

#### Step 3: Get Backend URL
```bash
gcloud run services describe vayudrishti-backend --region us-central1 --format 'value(status.url)'
```

#### Step 4: Update Frontend Environment
Edit `web-frontend/.env.production`:
```env
VITE_API_URL=<BACKEND_URL_FROM_STEP_3>
VITE_SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY
```

#### Step 5: Build and Deploy Frontend
```bash
cd web-frontend

# Build Docker image with backend URL
gcloud builds submit --tag gcr.io/gee-data-490807/vayudrishti-frontend \
  --substitutions=_BACKEND_URL=<BACKEND_URL_FROM_STEP_3>

# Deploy to Cloud Run
gcloud run deploy vayudrishti-frontend \
  --image gcr.io/gee-data-490807/vayudrishti-frontend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

#### Step 6: Get Frontend URL
```bash
gcloud run services describe vayudrishti-frontend --region us-central1 --format 'value(status.url)'
```

## Architecture

```
┌─────────────────┐
│   Cloud Run     │
│   (Frontend)    │
│   Port: 80      │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   Cloud Run     │
│   (Backend)     │
│   Port: 8080    │
└────────┬────────┘
         │
         ├──────────► Supabase (Database)
         ├──────────► Google Earth Engine
         └──────────► WAQI API
```

## Configuration

### Backend Environment Variables
- `WAQI_TOKEN`: Air quality API token
- `GCP_PROJECT_ID`: Google Cloud project ID
- `GCP_LOCATION`: Deployment region
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key

### Frontend Environment Variables
- `VITE_API_URL`: Backend API URL
- `VITE_SUPABASE_URL`: Supabase project URL
- `VITE_SUPABASE_ANON_KEY`: Supabase anon key

## Monitoring

### View Logs
```bash
# Backend logs
gcloud run services logs read vayudrishti-backend --region us-central1

# Frontend logs
gcloud run services logs read vayudrishti-frontend --region us-central1
```

### View Metrics
```bash
# Open Cloud Console
gcloud run services describe vayudrishti-backend --region us-central1
```

## Scaling

Cloud Run automatically scales based on traffic:
- **Min instances**: 1 (always warm)
- **Max instances**: 10
- **CPU allocation**: Only during request processing
- **Memory**: Backend 2GB, Frontend 512MB

## Cost Estimation

**Backend (2GB RAM, 2 vCPU):**
- ~$0.00002400 per second
- ~$2.07 per day (continuous)
- ~$62 per month (continuous)

**Frontend (512MB RAM, 1 vCPU):**
- ~$0.00000600 per second
- ~$0.52 per day (continuous)
- ~$15.50 per month (continuous)

**Total**: ~$77.50/month for continuous operation
**With auto-scaling**: Significantly less based on actual traffic

## Custom Domain (Optional)

1. **Map domain to Cloud Run:**
```bash
gcloud run domain-mappings create --service vayudrishti-frontend --domain yourdomain.com --region us-central1
```

2. **Update DNS records** as instructed by GCP

3. **Enable HTTPS** (automatic with Cloud Run)

## Troubleshooting

### Build Fails
- Check Docker files are present
- Verify all dependencies in requirements.txt
- Check Cloud Build logs: `gcloud builds list`

### Service Won't Start
- Check logs: `gcloud run services logs read <service-name>`
- Verify environment variables
- Check service account permissions

### Connection Issues
- Verify CORS settings in backend
- Check firewall rules
- Ensure Supabase allows connections from GCP

## Rollback

```bash
# List revisions
gcloud run revisions list --service vayudrishti-backend --region us-central1

# Rollback to previous revision
gcloud run services update-traffic vayudrishti-backend \
  --to-revisions <REVISION_NAME>=100 \
  --region us-central1
```

## CI/CD Setup (Optional)

### Connect to GitHub
1. Go to Cloud Build > Triggers
2. Connect your repository
3. Create trigger using `cloudbuild.yaml`
4. Auto-deploy on push to main branch

## Security Best Practices

1. **Use Secret Manager** for sensitive data:
```bash
echo -n "your-secret" | gcloud secrets create my-secret --data-file=-
```

2. **Enable VPC** for private networking
3. **Set up IAM roles** properly
4. **Enable Cloud Armor** for DDoS protection
5. **Use Cloud CDN** for static assets

## Support

- GCP Documentation: https://cloud.google.com/run/docs
- Cloud Build: https://cloud.google.com/build/docs
- Supabase: https://supabase.com/docs

## Next Steps

1. ✅ Deploy to GCP
2. Test all endpoints
3. Configure custom domain
4. Set up monitoring alerts
5. Enable Cloud CDN
6. Configure backup strategy
