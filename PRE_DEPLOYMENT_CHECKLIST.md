# Pre-Deployment Checklist ✓

## Before You Deploy

### 1. Google Cloud Setup
- [ ] GCP account created
- [ ] Billing enabled on project `gee-data-490807`
- [ ] Google Cloud SDK installed
- [ ] Authenticated: `gcloud auth login`
- [ ] Project set: `gcloud config set project gee-data-490807`

### 2. Verify Files Exist
- [ ] `backend/Dockerfile`
- [ ] `backend/requirements.txt`
- [ ] `backend/app/main.py`
- [ ] `web-frontend/Dockerfile`
- [ ] `web-frontend/package.json`
- [ ] `cloudbuild.yaml`

### 3. Environment Variables
- [ ] Supabase URL configured
- [ ] Supabase anon key configured
- [ ] WAQI token configured
- [ ] GCP project ID correct

### 4. Test Locally First
- [ ] Backend runs: `cd backend && python -m uvicorn app.main:app`
- [ ] Frontend runs: `cd web-frontend && npm run dev`
- [ ] Can create user
- [ ] Can submit complaint
- [ ] Map loads correctly

### 5. Code Quality
- [ ] No syntax errors
- [ ] All imports working
- [ ] Environment variables loaded
- [ ] CORS configured
- [ ] Authentication working

## Deployment Command

Once all checks pass:

```bash
deploy-simple.bat
```

## Expected Timeline

- API enablement: 1-2 minutes
- Backend build: 5-7 minutes
- Frontend build: 3-5 minutes
- Deployment: 2-3 minutes
- **Total**: 10-15 minutes

## What to Watch For

### During Build
- ✅ "Step 1/10" messages (Docker build)
- ✅ "Pushing image" messages
- ✅ "Deploying..." messages

### Success Indicators
- ✅ "Service [vayudrishti-backend] revision deployed"
- ✅ "Service [vayudrishti-frontend] revision deployed"
- ✅ URLs displayed at end

### Common Errors

**"Billing not enabled"**
- Fix: Enable billing in GCP Console

**"Permission denied"**
- Fix: `gcloud auth application-default login`

**"API not enabled"**
- Fix: Script will enable automatically

**"Build timeout"**
- Fix: Increase timeout in cloudbuild.yaml

## After Deployment

### Immediate Tests
1. Open frontend URL
2. Check landing page loads
3. Try to sign up
4. Try to log in
5. Submit a test complaint
6. Check map displays

### Verify Backend
```bash
curl https://YOUR-BACKEND-URL/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "waqi_configured": true,
  "gcp_configured": true
}
```

### Check Logs
```bash
# Backend logs
gcloud run services logs read vayudrishti-backend --region us-central1 --limit 50

# Frontend logs
gcloud run services logs read vayudrishti-frontend --region us-central1 --limit 50
```

## Rollback Plan

If deployment fails or app doesn't work:

1. **Check logs** for errors
2. **Fix issues** locally
3. **Test locally** again
4. **Redeploy**

Or rollback to previous version:
```bash
gcloud run revisions list --service vayudrishti-backend --region us-central1
gcloud run services update-traffic vayudrishti-backend --to-revisions PREVIOUS_REVISION=100
```

## Cost Monitoring

Set up budget alerts:
1. Go to: https://console.cloud.google.com/billing/budgets
2. Create budget: $100/month
3. Set alert at 50%, 90%, 100%

## Security Checklist

- [ ] HTTPS enforced (automatic)
- [ ] CORS configured correctly
- [ ] Environment variables not in code
- [ ] Supabase RLS enabled
- [ ] JWT authentication working
- [ ] No sensitive data in logs

## Performance Checklist

- [ ] Auto-scaling enabled
- [ ] Min instances: 1 (or 0 for cost savings)
- [ ] Max instances: 10
- [ ] Memory: Backend 2GB, Frontend 512MB
- [ ] CPU: Backend 2, Frontend 1

## Ready to Deploy?

If all checks pass, run:

```bash
deploy-simple.bat
```

## Need Help?

- Full guide: `GCP_DEPLOYMENT_GUIDE.md`
- Quick start: `DEPLOY_NOW.md`
- GCP Console: https://console.cloud.google.com
- Cloud Run Docs: https://cloud.google.com/run/docs

---

**Remember**: First deployment takes 10-15 minutes. Subsequent deployments are faster (5-7 minutes).

Good luck! 🚀
