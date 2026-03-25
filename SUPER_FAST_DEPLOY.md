# ⚡ Super Fast Deployment (3-5 Minutes!)

## The Fastest Way to Deploy Backend

Instead of waiting 15 minutes, use Cloud Run's direct source deployment:

```bash
deploy-backend-only.bat
```

This command:
- Builds directly from source (no separate Cloud Build step)
- Uses Cloud Run's built-in caching
- Deploys in 3-5 minutes instead of 15
- Keeps 1 instance always warm (no cold starts)

## What Changed?

### Before (15 minutes):
1. Upload to Cloud Build
2. Build Docker image
3. Push to Container Registry
4. Deploy to App Engine
5. Wait for App Engine to start

### Now (3-5 minutes):
1. Upload source to Cloud Run
2. Cloud Run builds and deploys directly
3. Done!

## Your Backend URLs

After deployment, you'll get a URL like:
```
https://vayudrishti-backend-[hash]-uc.a.run.app
```

## Update Frontend

Update `web-frontend/.env`:
```env
VITE_API_URL=https://vayudrishti-backend-[your-hash]-uc.a.run.app
```

## Even Faster: Skip Deployment

For development, just run locally:

```bash
# Terminal 1 - Backend (instant)
cd backend
uvicorn app.main:app --reload --port 8080

# Terminal 2 - Frontend (instant)
cd web-frontend
npm run dev
```

Frontend will be at: http://localhost:5173
Backend will be at: http://localhost:8080

## Cost

Cloud Run with `min-instances=1`:
- ~$5-10/month for always-on backend
- No cold starts
- Auto-scales to 10 instances if needed

## Troubleshooting

If deployment fails:
```bash
# Check Cloud Run logs
gcloud run services logs read vayudrishti-backend --region=us-central1 --project=gee-data-490807

# Test Docker build locally
cd backend
docker build -t test .
docker run -p 8080:8080 test
```

## Pro Tips

1. **Develop locally first** - Test everything before deploying
2. **Deploy only when ready** - Don't deploy every small change
3. **Use git branches** - Deploy from feature branches
4. **Monitor costs** - Check GCP billing dashboard

## Comparison

| Method | Time | Cost/Month | Use Case |
|--------|------|------------|----------|
| **Cloud Run (This)** | 3-5 min | $5-10 | Best for everything |
| App Engine | 15 min | $20-50 | Legacy, not recommended |
| Localhost | Instant | $0 | Development only |

## Next Steps

1. Run `deploy-backend-only.bat`
2. Wait 3-5 minutes
3. Copy the backend URL
4. Update frontend `.env`
5. Push to GitHub
6. Done!
