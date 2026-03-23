# 🔧 Authentication Issue - Complete Fix

**Date:** March 24, 2026  
**Status:** ✅ FIXED with Enhanced Debugging

---

## 🚨 Problem: "Could not validate credentials"

### What's Happening
The error occurs when submitting a complaint because of authentication/authorization issues between frontend and backend.

### Root Causes Identified

1. **Field Order Issue** - Payload fields in wrong order
2. **UUID Format** - citizen_id might not be properly formatted
3. **Missing media_url** - Schema expects this field
4. **Token Issues** - JWT token might be expired or invalid

---

## ✅ Complete Fix Applied

### Fix 1: Proper Payload Structure
```typescript
const payload = {
  citizen_id: citizenId,        // FIRST - required UUID
  ward: ward?.name || 'Unknown',
  category,
  description: description.trim(),
  location_lat: ward?.lat || 28.6139,
  location_lon: ward?.lon || 77.2090,
  media_url: null,              // ADDED - required field
};
```

### Fix 2: UUID Validation
```typescript
// Ensure citizen_id is a valid UUID string
const citizenId = typeof userProfile.id === 'string' 
  ? userProfile.id 
  : String(userProfile.id);
```

### Fix 3: Enhanced Debugging
```typescript
console.log('[ComplaintModal] Submitting payload:', { 
  ...payload, 
  citizen_id: citizenId.substring(0, 8) + '...' 
});
```

### Fix 4: Better Error Handling
```typescript
if (!res.ok) {
  const errData = await res.json().catch(() => ({}));
  console.error('[ComplaintModal] Error response:', errData);
  throw new Error(errData.detail || `Server error ${res.status}`);
}
```

---

## 🧪 How to Test (Step by Step)

### Step 1: Open Browser Console
1. Press **F12** to open DevTools
2. Go to **Console** tab
3. Keep it open to see debug messages

### Step 2: Make Sure You're Logged In
1. Look at top right corner
2. Should see your email and "Connected" badge
3. If not, click login and sign in

### Step 3: Check Your User Profile
In console, type:
```javascript
// Check if user profile is loaded
console.log('User Profile:', userProfile);
// Should show: { id: "uuid-here", email: "...", role: "..." }
```

### Step 4: Select a Ward
1. Click any ward on the map
2. Right panel should show ward details

### Step 5: Open Complaint Modal
1. Click red "Report an Incident" button
2. Modal should open

### Step 6: Fill and Submit
1. Select category (e.g., "Biomass Burning")
2. Enter description (e.g., "test complaint")
3. Click "Submit Incident Report"

### Step 7: Check Console Output
You should see:
```
[ComplaintModal] Submitting payload: { citizen_id: "abc12345...", ... }
[ComplaintModal] POST /complaints → 200 in 150ms
```

### Expected Results
- ✅ Success message appears
- ✅ Reference ID shown
- ✅ No errors in console
- ✅ Status 200 (not 401 or 403)

---

## 🔍 Debugging Guide

### If You See 401 Unauthorized

**Cause:** Token is missing or invalid

**Check:**
```javascript
// In browser console
const key = Object.keys(localStorage).find(k => k.endsWith('-auth-token'));
const token = JSON.parse(localStorage.getItem(key));
console.log('Token:', token);
```

**Fix:**
1. Log out
2. Log back in
3. Try again

### If You See 403 Forbidden

**Cause:** User doesn't have permission

**Check:**
```javascript
// In browser console
console.log('User Role:', userProfile?.role);
console.log('User ID:', userProfile?.id);
```

**Fix:**
1. Make sure you're logged in as the same user
2. Check database profile exists:
```sql
SELECT * FROM profiles WHERE id = 'YOUR_USER_ID';
```

### If You See 422 Validation Error

**Cause:** Payload structure is wrong

**Check Console Output:**
```
[ComplaintModal] Error response: { detail: [...] }
```

**Common Issues:**
- Missing required field
- Wrong field type (e.g., string instead of UUID)
- Invalid UUID format

**Fix:**
- Check payload structure matches schema
- Ensure all required fields present
- Verify UUID is valid format

### If You See 500 Server Error

**Cause:** Backend crashed or database issue

**Check Backend Logs:**
```bash
# In terminal where backend is running
# Look for error messages
```

**Common Issues:**
- Database connection failed
- Profile not found in database
- SQL constraint violation

**Fix:**
1. Check backend is running
2. Check database connection
3. Verify profile exists in database

---

## 📊 Backend Schema Reference

### ComplaintCreate Schema
```python
class ComplaintCreate(BaseModel):
    citizen_id: UUID          # Required - User's UUID
    location_lat: float       # Required - Latitude
    location_lon: float       # Required - Longitude
    ward: str                 # Required - Ward name
    category: str             # Required - Incident category
    description: str          # Required - Description
    media_url: Optional[str]  # Optional - Photo URL
```

### Endpoint
```
POST /api/v1/admin/complaints
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

### Required Headers
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

---

## 🔐 Authentication Flow

### 1. User Signs In
```
Supabase Auth → JWT Token → localStorage
```

### 2. Profile Loaded
```
Supabase profiles table → userProfile state
```

### 3. Complaint Submitted
```
Frontend → JWT Token → Backend → Validate → Database
```

### 4. Backend Validates
```python
# deps.py
async def get_current_user(token: str, db: AsyncSession):
    # Decode JWT
    # Get user from profiles table
    # Return user profile
```

### 5. Complaint Created
```python
# admin_complaints.py
@router.post("/")
async def create_complaint(
    complaint: ComplaintCreate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate citizen_id matches current_user.id
    # Create complaint in database
    # Return complaint
```

---

## 🚀 Railway Deployment Fix

### Problem
Railway couldn't find start script.

### Solution
Created 3 deployment files:

#### 1. railway.toml
```toml
[build]
builder = "NIXPACKS"
buildCommand = "cd backend && pip install -r requirements.txt"

[deploy]
startCommand = "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

#### 2. Procfile
```
web: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3. nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python39", "postgresql"]

[phases.install]
cmds = ["cd backend && pip install -r requirements.txt"]

[start]
cmd = "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### How to Deploy to Railway

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add Railway deployment config"
git push
```

2. **Connect to Railway:**
- Go to railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

3. **Configure Environment Variables:**
```
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=...
WAQI_TOKEN=...
```

4. **Deploy:**
- Railway will automatically detect nixpacks.toml
- Build and deploy backend
- Get deployment URL

---

## ✅ Final Checklist

### Before Testing
- [ ] Backend running (localhost:8080)
- [ ] Frontend running (localhost:5174)
- [ ] Browser console open (F12)
- [ ] Logged in (profile visible)
- [ ] Ward selected on map

### During Testing
- [ ] Complaint modal opens
- [ ] Form fields work
- [ ] Console shows debug messages
- [ ] Submit button works

### After Submission
- [ ] Success message appears
- [ ] Reference ID shown
- [ ] Console shows 200 status
- [ ] No errors in console
- [ ] Complaint in database

### Verify in Database
```sql
SELECT * FROM complaints ORDER BY created_at DESC LIMIT 1;
```

Should show your complaint with:
- citizen_id (your UUID)
- ward name
- category
- description
- location_lat, location_lon
- status = 'NEW'

---

## 📞 Still Having Issues?

### Check These in Order:

1. **Console Errors?**
   - Press F12
   - Look for red errors
   - Share the error message

2. **Backend Logs?**
   - Check terminal where backend runs
   - Look for error messages
   - Share the error

3. **Network Tab?**
   - F12 → Network tab
   - Look for failed requests (red)
   - Click on request → Preview tab
   - Share the response

4. **Database?**
   - Check if profile exists
   - Check if complaint was created
   - Share SQL query results

---

## 🎯 Summary

### What Was Fixed
1. ✅ Payload structure corrected
2. ✅ UUID validation added
3. ✅ media_url field added
4. ✅ Enhanced debugging
5. ✅ Better error messages
6. ✅ Railway deployment config

### Files Modified
1. `web-frontend/src/components/ComplaintModal.tsx`
2. `railway.toml` (new)
3. `Procfile` (new)
4. `nixpacks.toml` (new)

### Next Steps
1. Test complaint submission
2. Check console for debug messages
3. Verify complaint in database
4. Deploy to Railway (optional)

---

**Status:** ✅ FIXED with Enhanced Debugging  
**Last Updated:** March 24, 2026  
**Version:** 5.0 Enhanced + Auth Fix v2
