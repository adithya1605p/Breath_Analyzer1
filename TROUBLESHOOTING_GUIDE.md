# 🔧 Troubleshooting Guide

**Date:** March 24, 2026  
**Status:** Common Issues and Solutions

---

## 🚨 Issue: "Could not validate credentials"

### Symptoms
- Error appears when submitting a complaint
- Red error banner shows "Could not validate credentials"
- Complaint submission fails

### Root Causes
1. **User not logged in** - No authentication token available
2. **Token expired** - JWT token has expired (1 hour default)
3. **Invalid token** - Token format is incorrect
4. **Backend not running** - API server is down
5. **Database connection issue** - Profile not found in database

### Solutions

#### Solution 1: Log In First
**Steps:**
1. Look for the login/signup button in the top right
2. Click "Sign Up" or "Login"
3. Create an account or sign in
4. Wait for authentication to complete
5. Try submitting the complaint again

**How to verify:**
- You should see your name/email in the top right corner
- Profile icon should be visible

#### Solution 2: Refresh Token
**Steps:**
1. Log out (if logged in)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Close and reopen the browser
4. Log in again
5. Try submitting the complaint

**How to verify:**
```javascript
// Open browser console (F12) and run:
const key = Object.keys(localStorage).find(k => k.endsWith('-auth-token'));
const token = JSON.parse(localStorage.getItem(key));
console.log('Token:', token);
// Should show access_token and user info
```

#### Solution 3: Check Backend Connection
**Steps:**
1. Open `http://localhost:8080/docs` in a new tab
2. If it loads, backend is running
3. If it doesn't load, restart backend:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

#### Solution 4: Check Database Profile
**Steps:**
1. Get your user ID from localStorage (see Solution 2)
2. Connect to PostgreSQL:
```bash
psql -U postgres -d vayudrishti
```
3. Check if profile exists:
```sql
SELECT * FROM profiles WHERE id = 'YOUR_USER_ID';
```
4. If not found, insert profile:
```sql
INSERT INTO profiles (id, username, role, home_ward)
VALUES ('YOUR_USER_ID', 'your-email@example.com', 'citizen', 'Central Delhi');
```

#### Solution 5: Update Backend Code
The issue was fixed in the latest code. Make sure you have:
- `location_lat` and `location_lon` in payload (not `lat` and `lon`)
- Token validation check before API call
- User login check before submission

**Updated ComplaintModal.tsx:**
```typescript
// Check if user is logged in
if (!userProfile || !userProfile.id) {
  setError('You must be logged in to submit a complaint. Please sign in first.');
  return;
}

// Check if token exists
if (!token) {
  throw new Error('Authentication token not found. Please log in again.');
}

// Correct payload structure
const payload = {
  ward: ward?.name || 'Unknown',
  category,
  description: description.trim(),
  citizen_id: userProfile.id,
  location_lat: ward?.lat || 28.6139,
  location_lon: ward?.lon || 77.2090,
};
```

---

## 🚨 Issue: Landing Page Not Loading

### Symptoms
- Blank page or loading spinner
- Console errors about missing components
- "Cannot find module" errors

### Solutions

#### Solution 1: Check Import Path
Make sure `App.tsx` imports the correct landing page:
```typescript
import NationalIntelligenceLanding from './components/NationalIntelligenceLanding';
```

#### Solution 2: Verify File Exists
Check that the file exists:
```bash
ls web-frontend/src/components/NationalIntelligenceLanding.tsx
```

#### Solution 3: Restart Dev Server
```bash
cd web-frontend
npm run dev
```

---

## 🚨 Issue: Material Symbols Icons Not Showing

### Symptoms
- Icons appear as text (e.g., "security", "monitoring")
- Missing icon glyphs

### Solutions

#### Solution 1: Check Font Import
Verify `index.html` has the font link:
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,300,0,0&display=swap" rel="stylesheet" />
```

#### Solution 2: Check CSS Class
Icons should use:
```html
<span className="material-symbols-outlined">security</span>
```

#### Solution 3: Clear Cache
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Or clear browser cache completely

---

## 🚨 Issue: Admin Panel Shows Errors

### Symptoms
- "Failed to load complaints"
- "Failed to escalate Policy to Action Grid"
- Access denied messages

### Solutions

See `ADMIN_SETUP_GUIDE.md` for complete instructions.

**Quick Fix:**
1. Get your user ID from localStorage
2. Update database:
```sql
UPDATE profiles SET role = 'admin' WHERE id = 'YOUR_USER_ID';
```
3. Refresh the page
4. Navigate to `/admin`

---

## 🚨 Issue: Map Not Loading

### Symptoms
- Gray box instead of map
- "Failed to load ward data" error
- Empty map area

### Solutions

#### Solution 1: Check Backend API
1. Open `http://localhost:8080/api/v1/dashboard/wards`
2. Should return JSON with ward data
3. If error, check backend logs

#### Solution 2: Check CORS
Backend should allow frontend origin:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Solution 3: Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Refresh page
4. Look for failed requests (red)
5. Check error messages

---

## 🚨 Issue: Forecast Chart Not Displaying

### Symptoms
- Empty chart area
- Loading spinner forever
- "Forecast unavailable" error

### Solutions

#### Solution 1: Select a Ward First
- Click on a ward on the map
- Forecast loads for selected ward only

#### Solution 2: Check API Endpoint
```bash
curl http://localhost:8080/api/v1/dashboard/forecast?lat=28.6139&lon=77.2090
```
Should return JSON with forecast data.

#### Solution 3: Check Recharts Import
Verify `package.json` has:
```json
"recharts": "^2.x.x"
```

---

## 🚨 Issue: Satellite Data Not Loading

### Symptoms
- "Satellite Link Failed" error
- Long loading time (>10 seconds)
- "Querying Sentinel-5P satellite..." forever

### Solutions

#### Solution 1: Check Google Earth Engine Credentials
```bash
# Check if credentials file exists
ls backend/app/services/gee-data-490807-df45431ef2de.json
```

#### Solution 2: Check GEE Authentication
Backend logs should show:
```
[GEE] Earth Engine Service Account Authenticated for Project gee-data-490807
```

If not, check:
- Credentials file path in code
- Service account permissions
- GEE API enabled in Google Cloud

#### Solution 3: Timeout Issue
GEE can be slow. Increase timeout:
```typescript
// In LeafletMap or wherever GEE is called
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 seconds

fetch(url, { signal: controller.signal })
```

---

## 🚨 Issue: Database Connection Failed

### Symptoms
- "Failed to connect to database" error
- Backend crashes on startup
- "Connection refused" errors

### Solutions

#### Solution 1: Check PostgreSQL Running
```bash
# Windows
services.msc
# Look for PostgreSQL service

# Linux/Mac
sudo systemctl status postgresql
```

#### Solution 2: Check Database Exists
```bash
psql -U postgres -l
# Should list vayudrishti database
```

#### Solution 3: Check Connection String
```bash
# backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/vayudrishti
```

#### Solution 4: Create Database
```bash
psql -U postgres
CREATE DATABASE vayudrishti;
\q
```

---

## 🚨 Issue: Model Predictions Inaccurate

### Symptoms
- AQI values seem wrong
- Predictions don't match reality
- Large errors compared to WAQI

### Solutions

#### Solution 1: Check Model File
```bash
# Should exist and be ~774 KB
ls -lh backend/vayu_model_v5_best.pt
```

#### Solution 2: Check Scaler and Encoder
```bash
ls backend/vayu_scaler_v5.pkl
ls backend/vayu_label_encoder_v5.pkl
```

#### Solution 3: Retrain Model
If model is outdated:
```bash
cd backend
python train_v5_enhanced.py
```

#### Solution 4: Check Feature Count
Model expects 29 features. Verify in code:
```python
# backend/app/services/ml_engine.py
feature_cols = [
    # Should have 29 features total
]
```

---

## 🚨 Issue: Performance Slow

### Symptoms
- Page loads slowly (>5 seconds)
- API responses slow (>1 second)
- UI feels laggy

### Solutions

#### Solution 1: Enable Caching
```python
# backend/app/main.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

#### Solution 2: Optimize Database Queries
```sql
-- Add indexes
CREATE INDEX idx_complaints_citizen ON complaints(citizen_id);
CREATE INDEX idx_complaints_ward ON complaints(ward);
CREATE INDEX idx_complaints_status ON complaints(status);
```

#### Solution 3: Enable Frontend Code Splitting
```typescript
// Use lazy loading
const AdminGate = lazy(() => import('./admin/AdminGate'));
const ComplaintModal = lazy(() => import('./components/ComplaintModal'));
```

#### Solution 4: Compress Images
```bash
# Install imagemin
npm install -g imagemin-cli

# Compress images
imagemin web-frontend/public/*.png --out-dir=web-frontend/public/optimized
```

---

## 🚨 Issue: Mobile View Broken

### Symptoms
- Layout broken on mobile
- Text too small
- Buttons not clickable
- Horizontal scroll

### Solutions

#### Solution 1: Check Viewport Meta Tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

#### Solution 2: Test Responsive Design
- Open DevTools (F12)
- Click device toolbar icon
- Test different screen sizes

#### Solution 3: Fix Tailwind Classes
Use responsive classes:
```html
<div className="text-sm md:text-base lg:text-lg">
```

---

## 🔍 Debugging Tools

### Browser Console
```javascript
// Check authentication
const key = Object.keys(localStorage).find(k => k.endsWith('-auth-token'));
console.log('Token:', JSON.parse(localStorage.getItem(key)));

// Check API base URL
console.log('API URL:', import.meta.env.VITE_API_URL);

// Check user profile
console.log('User:', userProfile);
```

### Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Look for failed requests (red)
5. Click on request to see details

### Backend Logs
```bash
# Watch backend logs in real-time
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080 --log-level debug
```

### Database Queries
```sql
-- Check recent complaints
SELECT * FROM complaints ORDER BY created_at DESC LIMIT 10;

-- Check user profiles
SELECT id, username, role FROM profiles;

-- Check tasks
SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10;
```

---

## 📞 Getting Help

### Check Documentation
1. `ADMIN_SETUP_GUIDE.md` - Admin panel setup
2. `DEPLOYMENT_AND_FEATURES_PLAN.md` - Deployment guide
3. `SESSION_11_SUMMARY.md` - Latest changes
4. `WHATS_NEXT.md` - Action items

### Check Logs
1. **Frontend:** Browser console (F12)
2. **Backend:** Terminal where uvicorn is running
3. **Database:** PostgreSQL logs

### Common Commands
```bash
# Restart frontend
cd web-frontend
npm run dev

# Restart backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Check database
psql -U postgres -d vayudrishti

# Clear cache
# Browser: Ctrl+Shift+Delete
# npm: npm cache clean --force
```

---

## ✅ Quick Checklist

When something goes wrong:
- [ ] Check browser console for errors (F12)
- [ ] Check backend logs in terminal
- [ ] Verify backend is running (localhost:8080/docs)
- [ ] Verify frontend is running (localhost:5174)
- [ ] Check if logged in (profile icon visible)
- [ ] Try logging out and back in
- [ ] Clear browser cache
- [ ] Restart both servers
- [ ] Check database connection
- [ ] Review recent code changes

---

**Status:** Comprehensive Troubleshooting Guide  
**Last Updated:** March 24, 2026  
**Version:** 1.0
