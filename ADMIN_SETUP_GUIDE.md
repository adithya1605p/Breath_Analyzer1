# 🔐 Admin Panel Setup Guide

**Date:** March 24, 2026  
**Status:** Complete Setup Instructions

---

## 🎯 Overview

The VayuDrishti admin panel requires proper authentication and role assignment. This guide will help you set up admin access.

---

## 📋 Prerequisites

1. ✅ Backend running on `http://localhost:8080`
2. ✅ Frontend running on `http://localhost:5174`
3. ✅ PostgreSQL database configured
4. ✅ Supabase authentication enabled

---

## 🔧 Setup Steps

### Step 1: Create a User Account

1. Go to `http://localhost:5174`
2. Click "Sign Up" or "Login"
3. Create an account with your email
4. Complete the registration process

### Step 2: Get Your User ID

After logging in, open the browser console (F12) and run:

```javascript
// Get your Supabase session
const key = Object.keys(localStorage).find(k => k.endsWith('-auth-token'));
const token = JSON.parse(localStorage.getItem(key));
console.log('Your User ID:', token.user.id);
```

Copy the User ID (it's a UUID like `123e4567-e89b-12d3-a456-426614174000`)

### Step 3: Update Database Role

You need to manually set your role to 'admin' or 'officer' in the database.

#### Option A: Using SQL (Recommended)

Connect to your PostgreSQL database and run:

```sql
-- Check if profile exists
SELECT * FROM profiles WHERE id = 'YOUR_USER_ID_HERE';

-- If profile exists, update role
UPDATE profiles 
SET role = 'admin' 
WHERE id = 'YOUR_USER_ID_HERE';

-- If profile doesn't exist, insert it
INSERT INTO profiles (id, username, role, home_ward)
VALUES (
    'YOUR_USER_ID_HERE',
    'your-email@example.com',
    'admin',
    'Central Delhi'
);
```

#### Option B: Using Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to "Table Editor"
3. Open the `profiles` table
4. Find your user ID or create a new row
5. Set `role` to `'admin'` or `'officer'`
6. Save changes

### Step 4: Verify Access

1. Refresh the page (`http://localhost:5174`)
2. Navigate to `/admin` route
3. You should see the admin dashboard

---

## 🚨 Troubleshooting

### Error: "Failed to load complaints"

**Cause:** Backend API not responding or authentication issue

**Solutions:**
1. Check backend is running: `http://localhost:8080/docs`
2. Verify your token in localStorage
3. Check browser console for error messages
4. Ensure database connection is working

### Error: "Failed to escalate Policy to Action Grid"

**Cause:** Task creation endpoint requires admin authentication

**Solutions:**
1. Verify your role is 'admin' or 'officer' in database
2. Check the backend logs for errors
3. Ensure the `/api/v1/admin/tasks` endpoint is working

### Error: "ACCESS DENIED: Required security clearance not found"

**Cause:** Your user profile doesn't have admin role

**Solutions:**
1. Follow Step 3 above to update your role
2. Make sure you're using the correct User ID
3. Refresh the page after updating the database

### Error: "Could not validate credentials"

**Cause:** JWT token is invalid or expired

**Solutions:**
1. Log out and log back in
2. Clear localStorage and re-authenticate
3. Check Supabase project settings

---

## 🔑 Role Types

### Citizen (Default)
- Can view their home ward only
- Can submit complaints
- Can view their own complaints
- Limited access

### Officer
- Can view all wards
- Can manage complaints
- Can create tasks
- Can view analytics
- Admin panel access

### Admin (Full Access)
- All officer permissions
- Can manage users
- Can view audit logs
- Full system access

---

## 📊 Admin Panel Features

### 1. Live Monitoring (`/admin`)
- Real-time ward statistics
- AQI heatmap
- System health metrics

### 2. Complaints Panel (`/admin/complaints`)
- View all citizen complaints
- Filter by status, ward
- Update complaint status
- Add internal notes
- Assign to officers

### 3. Tasks Board (`/admin/tasks`)
- Create and manage tasks
- Assign to team members
- Track progress
- Set priorities and deadlines

### 4. Policy Hub (`/admin/reports`)
- AI-generated policy recommendations
- Escalate policies to action tasks
- View Vertex AI insights

---

## 🔐 Security Notes

### Authentication Flow

1. User logs in via Supabase Auth
2. Supabase returns JWT token
3. Frontend stores token in localStorage
4. Backend validates JWT on each request
5. Backend checks user role in `profiles` table
6. Access granted/denied based on role

### Token Storage

Tokens are stored in localStorage with key format:
```
sb-[project-ref]-auth-token
```

### API Authentication

All admin endpoints require:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 🧪 Testing Admin Access

### Test Complaints Endpoint

```bash
# Get your token from localStorage first
curl -X GET "http://localhost:8080/api/v1/admin/complaints" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected response: Array of complaints

### Test Tasks Endpoint

```bash
curl -X POST "http://localhost:8080/api/v1/admin/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "Testing admin access",
    "priority": "MEDIUM"
  }'
```

Expected response: Created task object

---

## 📝 Database Schema

### Profiles Table

```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY,
    username VARCHAR UNIQUE,
    role VARCHAR DEFAULT 'citizen',
    home_ward VARCHAR
);
```

### Complaints Table

```sql
CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    citizen_id UUID REFERENCES profiles(id),
    location_lat FLOAT NOT NULL,
    location_lon FLOAT NOT NULL,
    ward VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    media_url VARCHAR,
    status VARCHAR DEFAULT 'NEW',
    assigned_to UUID REFERENCES profiles(id),
    internal_notes VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    complaint_id UUID REFERENCES complaints(id),
    assignee_id UUID REFERENCES profiles(id),
    title VARCHAR NOT NULL,
    description VARCHAR,
    priority VARCHAR DEFAULT 'MEDIUM',
    status VARCHAR DEFAULT 'PENDING',
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

---

## 🚀 Quick Start Commands

### Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Start Frontend
```bash
cd web-frontend
npm run dev
```

### Access Admin Panel
```
http://localhost:5174/admin
```

---

## 📞 Support

If you encounter issues:

1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify database connection
4. Ensure Supabase project is active
5. Check environment variables in `.env` files

---

## ✅ Checklist

Before accessing admin panel:

- [ ] Backend running on port 8080
- [ ] Frontend running on port 5174
- [ ] User account created
- [ ] User ID obtained
- [ ] Role set to 'admin' or 'officer' in database
- [ ] Page refreshed after role update
- [ ] Token valid (not expired)
- [ ] Database connection working

---

**Status:** Ready for Admin Access  
**Last Updated:** March 24, 2026  
**Version:** 1.0
