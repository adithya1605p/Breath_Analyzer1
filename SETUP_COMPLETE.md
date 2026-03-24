# ✅ Supabase Configuration Complete!

## What I Just Did

1. ✅ Updated `web-frontend/.env` with your Supabase credentials
2. ✅ Updated `backend/.env` with Supabase configuration

## Next Steps (2 minutes)

### Step 1: Get Your Database Password

1. Go to https://supabase.com/dashboard
2. Select your project: `tmavkmymbdcmugunjtle`
3. Go to **Settings** → **Database**
4. Copy your **Database Password**

### Step 2: Update Backend .env

Open `backend/.env` and replace `your-password-here` with your actual password:

```env
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.tmavkmymbdcmugunjtle.supabase.co:5432/postgres
```

### Step 3: Set Up Database Tables

Run the SQL schema in Supabase:

1. Go to **SQL Editor** in Supabase dashboard
2. Run this SQL:

```sql
-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    username TEXT UNIQUE,
    role TEXT DEFAULT 'citizen',
    home_ward TEXT
);

-- Create complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    citizen_id UUID REFERENCES profiles(id),
    location_lat FLOAT NOT NULL,
    location_lon FLOAT NOT NULL,
    ward TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    media_url TEXT,
    status TEXT DEFAULT 'NEW',
    assigned_to UUID REFERENCES profiles(id),
    internal_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_id UUID REFERENCES complaints(id),
    assignee_id UUID REFERENCES profiles(id),
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'MEDIUM',
    status TEXT DEFAULT 'PENDING',
    deadline TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ward TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    severity TEXT DEFAULT 'HIGH',
    is_acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID REFERENCES profiles(id),
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view their own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Anyone can view complaints" ON complaints
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create complaints" ON complaints
    FOR INSERT WITH CHECK (auth.uid() = citizen_id);
```

### Step 4: Restart Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Terminal 2 - Frontend:**
```bash
cd web-frontend
npm run dev
```

### Step 5: Test It!

1. Go to `http://localhost:5174`
2. You should see a **login/signup form**
3. Create an account
4. After login, try submitting a complaint
5. Should work now! ✅

---

## What's Configured

### Frontend (.env)
```env
VITE_API_URL=http://192.168.0.137:8080
VITE_SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGci...
```

### Backend (.env)
```env
SUPABASE_URL=https://tmavkmymbdcmugunjtle.supabase.co
SUPABASE_KEY=eyJhbGci...
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.tmavkmymbdcmugunjtle.supabase.co:5432/postgres
```

---

## Troubleshooting

### If login form doesn't appear:
- Restart frontend: `npm run dev`
- Clear browser cache: Ctrl+Shift+Delete
- Check console for errors

### If "Could not validate credentials" still appears:
- Make sure you're logged in (see profile in top right)
- Check DATABASE_URL has correct password
- Verify tables exist in Supabase

### If backend crashes:
- Check DATABASE_URL is correct
- Make sure Supabase project is active
- Check backend logs for errors

---

## Quick Test

After setup, test authentication:

1. **Sign Up:**
   - Email: test@example.com
   - Password: Test123456!

2. **Check Profile:**
   - Should see email in top right
   - Should see "Connected" badge

3. **Submit Complaint:**
   - Select a ward
   - Click "Report an Incident"
   - Fill form and submit
   - Should get success message!

---

**Status:** ✅ Configuration Complete  
**Next:** Set up database and restart servers  
**Time:** 2 minutes
