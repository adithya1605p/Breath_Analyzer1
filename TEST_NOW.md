# ✅ Servers Restarted - Test Now!

## Both servers are running with new configuration:

- ✅ Frontend: `http://localhost:5174`
- ✅ Backend: `http://localhost:8080`
- ✅ Supabase configured
- ✅ Environment variables loaded

---

## Test Steps:

### 1. Open the App
Go to: `http://localhost:5174`

### 2. What You Should See
- **Landing page** with "National Air Intelligence System"
- **Click "Enter Command Center"** button
- You should see a **login/signup form** overlay

### 3. Sign Up
- Email: `test@example.com`
- Password: `Test123456!`
- Click "Sign Up"

### 4. After Login
- You should see your email in the top right corner
- "Connected" badge should appear
- Map should load with wards

### 5. Submit Complaint
- Click on any ward on the map
- Click "Report an Incident" (red button)
- Fill in:
  - Category: Biomass Burning
  - Description: test
- Click "Submit Incident Report"
- **Should work now!** ✅

---

## If Still Getting "Could not validate credentials"

### Check Browser Console (F12):
Look for these messages:
- `[ComplaintModal] Submitting payload: ...`
- `[ComplaintModal] POST /complaints → 200`

### If you see 401 errors:
1. Make sure you're logged in (see email in top right)
2. Try logging out and back in
3. Clear browser cache (Ctrl+Shift+Delete)

### If login form doesn't appear:
1. Hard refresh: Ctrl+Shift+R
2. Check console for errors
3. Verify `.env` file has Supabase credentials

---

## Quick Debug

Open browser console (F12) and run:
```javascript
console.log('Supabase URL:', import.meta.env.VITE_SUPABASE_URL);
console.log('API URL:', import.meta.env.VITE_API_URL);
```

Should show:
```
Supabase URL: https://tmavkmymbdcmugunjtle.supabase.co
API URL: http://192.168.0.137:8080
```

---

**Try it now! The servers are restarted with the correct configuration.** 🚀
