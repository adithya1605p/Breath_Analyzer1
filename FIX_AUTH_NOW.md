# 🔥 URGENT FIX - Authentication Not Configured

## The Problem
You're getting "Could not validate credentials" because **Supabase is not set up**.

## The Solution (2 minutes)

### Option 1: Set Up Supabase (Recommended)

1. **Go to** https://supabase.com
2. **Sign up** for free account
3. **Create new project**
4. **Get your credentials:**
   - Project URL: `https://xxxxx.supabase.co`
   - Anon Key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

5. **Update `web-frontend/.env`:**
```env
VITE_API_URL=http://192.168.0.137:8080
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

6. **Restart frontend:**
```bash
cd web-frontend
npm run dev
```

7. **Now you can log in!**

---

### Option 2: Use Backend Without Auth (Quick Test)

If you just want to test without setting up Supabase:

1. **Modify backend to allow anonymous complaints**

Create `backend/app/api/endpoints/public_complaints.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.admin_models import Complaint
import uuid

router = APIRouter()

@router.post("/public/complaint")
async def create_public_complaint(
    ward: str,
    category: str,
    description: str,
    lat: float,
    lon: float,
    db: AsyncSession = Depends(get_db)
):
    # Create anonymous complaint
    complaint = Complaint(
        id=uuid.uuid4(),
        citizen_id=uuid.uuid4(),  # Anonymous user
        ward=ward,
        category=category,
        description=description,
        location_lat=lat,
        location_lon=lon,
        status='NEW'
    )
    db.add(complaint)
    await db.commit()
    await db.refresh(complaint)
    return {"id": str(complaint.id), "status": "success"}
```

2. **Register the router in `backend/app/main.py`:**
```python
from app.api.endpoints import public_complaints

app.include_router(public_complaints.router, prefix="/api/v1", tags=["public"])
```

3. **Update frontend to use public endpoint** (temporary)

---

## Why This Happened

Your `.env` file only had:
```env
VITE_API_URL=http://192.168.0.137:8080
```

It was missing:
```env
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...
```

Without these, the app can't authenticate users, so:
- No login button works
- No auth token
- All API calls fail with 401

---

## Quick Check

After setting up Supabase, you should see:
1. ✅ Login/Signup form on the page
2. ✅ Ability to create account
3. ✅ Profile icon after login
4. ✅ Complaints submit successfully

---

## Need Help?

**Get Supabase credentials:**
1. Go to https://supabase.com
2. Sign in
3. Create project (takes 2 minutes)
4. Go to Settings → API
5. Copy "Project URL" and "anon public" key
6. Paste into `.env` file
7. Restart frontend

**That's it!** 🚀
