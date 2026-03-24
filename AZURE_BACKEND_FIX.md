# Azure Backend Fix Guide

## Current Status: 503 Server Unavailable ❌

Your Azure backend at `https://vayudrishti-f9bnd4c4h7enffb5.centralindia-01.azurewebsites.net/` is not responding.

## Likely Issues:

### 1. Missing Environment Variables in Azure
The backend needs these environment variables configured in Azure:

```bash
WAQI_TOKEN=9abbe99f4595fa8a4d20dd26a06db8e375273034
GCP_PROJECT_ID=gee-data-490807
GCP_LOCATION=us-central1
SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY
VITE_SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY
```

### 2. How to Add Environment Variables in Azure:

#### Option A: Azure Portal
1. Go to https://portal.azure.com
2. Navigate to your App Service: `vayudrishti-f9bnd4c4h7enffb5`
3. Click **Configuration** in the left menu
4. Click **+ New application setting**
5. Add each environment variable above
6. Click **Save** at the top
7. Click **Continue** to restart the app

#### Option B: Azure CLI
```bash
az webapp config appsettings set --name vayudrishti-f9bnd4c4h7enffb5 --resource-group <your-resource-group> --settings \
  WAQI_TOKEN="9abbe99f4595fa8a4d20dd26a06db8e375273034" \
  GCP_PROJECT_ID="gee-data-490807" \
  GCP_LOCATION="us-central1" \
  SUPABASE_URL="https://tmavkmymbdcmugunjtle.supabase.co" \
  SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY" \
  VITE_SUPABASE_URL="https://tmavkmymbdcmugunjtle.supabase.co" \
  VITE_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtYXZrbXltYmRjbXVndW5qdGxlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMzAyMDYsImV4cCI6MjA4OTYwNjIwNn0.BEr2krViE54HjVtmm-WD6KV7cIcDQMOSmM-VyjiH7cY"
```

### 3. Check Application Logs

To see what's causing the 503 error:

1. Go to Azure Portal → Your App Service
2. Click **Log stream** in the left menu
3. Look for error messages

Or use Azure CLI:
```bash
az webapp log tail --name vayudrishti-f9bnd4c4h7enffb5 --resource-group <your-resource-group>
```

### 4. Common Issues:

#### Issue: Port Configuration
Azure expects the app to listen on port 8000 or use the `PORT` environment variable.

**Fix**: Our Dockerfile already handles this with `PORT=8080`, but Azure might need:
- Add environment variable: `PORT=8000`
- Or update startup command to use Azure's default port

#### Issue: Missing GCP Credentials
The app tries to load `ee-credentials.json` for Google Earth Engine.

**Fix**: Either:
1. Upload the credentials file to Azure
2. Or disable GEE features if not needed

#### Issue: Startup Timeout
The ML model loading might take too long.

**Fix**: Increase startup timeout in Azure:
```bash
az webapp config set --name vayudrishti-f9bnd4c4h7enffb5 --resource-group <your-resource-group> --startup-time 600
```

### 5. Quick Test After Fixing:

```bash
# Test health endpoint
curl https://vayudrishti-f9bnd4c4h7enffb5.centralindia-01.azurewebsites.net/health

# Should return:
# {"status":"healthy","version":"0.1.0",...}
```

### 6. Update Vercel Frontend:

Once backend is working, update Vercel environment variable:
```
VITE_API_URL=https://vayudrishti-f9bnd4c4h7enffb5.centralindia-01.azurewebsites.net
```

Then redeploy Vercel frontend.

## Alternative: Use Railway or Render

If Azure continues to have issues, you can deploy to:
- **Railway**: Already configured in `railway.json`
- **Render**: Free tier available
- **GCP Cloud Run**: We have the configuration ready

## Need Help?

1. Check Azure logs first (most important!)
2. Verify all environment variables are set
3. Check if the app is using the correct port
4. Ensure startup command is correct

---

**Current Status**: Backend is DOWN (503)
**Next Step**: Add environment variables in Azure Portal
**Expected Time**: 5-10 minutes to fix
