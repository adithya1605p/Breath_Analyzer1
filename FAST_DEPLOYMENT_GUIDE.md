# ⚡ Fast Backend Deployment Guide

## Why It's Faster Now

1. **Docker Layer Caching**: Reuses previously built layers
2. **Cloud Run Instead of App Engine**: Deploys in ~3-5 minutes vs 15 minutes
3. **Optimized Build Machine**: Uses E2_HIGHCPU_8 for faster builds
4. **Minimal Logging**: Only essential logs to speed up process

## Quick Deploy (3-5 minutes)

```bash
# Windows
deploy-fast.bat

# Or manually
cd backend
gcloud builds submit --config=../cloudbuild-fast.yaml --project=gee-data-490807
```

## Get Your Backend URL

```bash
gcloud run services describe vayudrishti-backend --region=us-central1 --format="value(status.url)"
```

## Update Frontend to Use New Backend

After deployment, update your frontend `.env`:

```env
VITE_API_URL=https://vayudrishti-backend-[your-hash].run.app
```

## Even Faster: Local Development

For rapid iteration, use localhost:

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8080

# Terminal 2 - Frontend
cd web-frontend
npm run dev
```

## Deployment Comparison

| Method | Time | Use Case |
|--------|------|----------|
| **Cloud Run (Fast)** | 3-5 min | Quick updates, testing |
| App Engine | 15 min | Production, auto-scaling |
| Localhost | Instant | Development |

## Tips for Faster Workflow

1. **Develop Locally First**: Test everything on localhost
2. **Deploy Only When Ready**: Don't deploy every small change
3. **Use Git Branches**: Deploy from specific branches
4. **Monitor Builds**: Watch Cloud Build console for issues

## Troubleshooting

If deployment fails:
1. Check Cloud Build logs in GCP Console
2. Verify Docker builds locally: `docker build -t test ./backend`
3. Ensure all environment variables are set
4. Check Cloud Run quotas in your project

## Cost Optimization

Cloud Run charges only for:
- Request time (not idle time)
- Memory used during requests
- Network egress

With `min-instances=1`, you'll have ~$5-10/month for always-on backend.
