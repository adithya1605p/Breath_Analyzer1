# VayuDrishti - Quick Reference Guide

**Last Updated:** March 23, 2026

---

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit with your credentials
docker-compose up -d  # Start TimescaleDB
python -m app.main    # Start FastAPI server (port 8080)
```

### Frontend Setup
```bash
cd web-frontend
npm install
cp .env.example .env  # Edit with your API URL
npm run dev          # Start Vite dev server (port 5173)
```

---

## 📁 Project Structure

```
VayuDrishti/
├── backend/
│   ├── app/
│   │   ├── ai/              # A3T-GCN neural network
│   │   ├── api/endpoints/   # FastAPI routes
│   │   ├── core/            # Config, Celery
│   │   ├── db/              # Database models
│   │   ├── services/        # ML, GEE, routing
│   │   └── main.py          # Entry point
│   ├── data/                # Model weights, graphs
│   ├── cache/               # API response cache
│   └── docker-compose.yml   # TimescaleDB
│
├── web-frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app
│   │   └── supabaseClient.ts
│   └── public/              # GeoJSON data
│
├── HARDCODED_VALUES_AUDIT.md  # Security audit
├── AUDIT_SESSION_LOG.md       # What was done
└── README.md                  # Project overview
```

---

## 🔑 Environment Variables

### Backend (.env)
```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong-password>
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=breath_analyzer

# External APIs
WAQI_TOKEN=<your-waqi-token>
GCP_PROJECT_ID=<your-gcp-project>
GCP_LOCATION=us-central1

# Supabase
VITE_SUPABASE_URL=<your-supabase-url>
VITE_SUPABASE_ANON_KEY=<your-supabase-key>

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8080
VITE_SUPABASE_URL=<your-supabase-url>
VITE_SUPABASE_ANON_KEY=<your-supabase-key>
```

---

## 🌐 API Endpoints

### Dashboard
- `GET /api/v1/dashboard/wards?level=ward` - Get ward-level AQI data
- `GET /api/v1/dashboard/recommendations` - AI policy recommendations
- `GET /api/v1/dashboard/forecast?lat=X&lon=Y` - 8-day PM2.5 forecast

### Satellite
- `GET /api/v1/gee/analyze?lat=X&lon=Y` - Sentinel-5P analysis

### Navigation
- `GET /api/v1/navigation/route?start_lat=X&start_lon=Y&end_lat=X&end_lon=Y&health_sensitivity=50`

### Users
- `GET /api/v1/users/complaints` - User's complaints
- `GET /api/v1/users/{username}/exposure` - Safe exposure time

### Admin
- `GET /api/v1/admin/alerts` - System alerts
- `POST /api/v1/admin/complaints` - Assign complaints

---

## 🗄️ Database Schema

### sensor_data (TimescaleDB)
```sql
time          TIMESTAMP WITH TIME ZONE
sensor_id     VARCHAR(50)
latitude      FLOAT
longitude     FLOAT
pm25          FLOAT
pm10          FLOAT
no2           FLOAT
so2           FLOAT
co            FLOAT
o3            FLOAT
```

### profiles
```sql
id            UUID
username      VARCHAR
role          VARCHAR (citizen/officer/admin)
home_ward     VARCHAR
```

### complaints
```sql
id            UUID
citizen_id    UUID
location_lat  FLOAT
location_lon  FLOAT
ward          VARCHAR
category      VARCHAR
description   VARCHAR
status        ENUM (NEW/UNDER_REVIEW/IN_ACTION/RESOLVED/REJECTED)
```

---

## 🤖 ML Models

### A3T-GCN (Routing)
- **Location:** `backend/app/data/a3tgcn_weights.pt`
- **Purpose:** Predict PM2.5 on road segments
- **Input:** 5 node features, 24-hour sequence
- **Output:** PM2.5 prediction per node

### Temporal Neural Network (Spatial Interpolation)
- **Location:** `backend/app/services/vayu_spatial_PRODUCTION.pt`
- **Purpose:** Interpolate PM2.5 for blind zones
- **Input:** 7 features (lat, lon, distance, co, no2, pm10, so2)
- **Output:** PM2.5 prediction
- **Scaler:** `vayu_scaler.pkl` (StandardScaler)

---

## 🛰️ External Services

### WAQI (World Air Quality Index)
- **Purpose:** Real-time AQI data
- **Endpoint:** `https://api.waqi.info/`
- **Rate Limit:** Check your plan
- **Docs:** https://aqicn.org/api/

### OpenAQ
- **Purpose:** Government sensor data
- **Endpoint:** `https://api.openaq.org/v3`
- **Rate Limit:** 10,000 requests/day (free tier)
- **Docs:** https://docs.openaq.org/

### Google Earth Engine
- **Purpose:** Sentinel-5P satellite data
- **Collections:** 
  - `COPERNICUS/S5P/NRTI/L3_AER_AI` (Aerosol)
  - `COPERNICUS/S5P/NRTI/L3_CO` (Carbon Monoxide)
- **Auth:** Service account JSON
- **Docs:** https://developers.google.com/earth-engine

### Vertex AI (Gemini)
- **Purpose:** Policy recommendations
- **Model:** `gemini-3-pro-preview`
- **Region:** `global` (experimental)
- **Docs:** https://cloud.google.com/vertex-ai/docs

### Supabase
- **Purpose:** Authentication, user profiles
- **Features:** Auth, REST API, Realtime
- **Docs:** https://supabase.com/docs

---

## 🔧 Common Tasks

### Rotate API Keys
1. Generate new keys from service providers
2. Update `.env` files
3. Restart backend server
4. Test all integrations

### Add New City
1. Update geographic bounds in `dashboard.py`
2. Add GeoJSON file to `web-frontend/public/`
3. Update city center coordinates
4. Download OSM graph for routing
5. Test all endpoints

### Update ML Model
1. Train new model (see `train_vayu_v2.py`)
2. Save weights to `backend/app/services/`
3. Update model path in `ml_engine.py`
4. Restart backend
5. Verify predictions

### Deploy to Production
1. **Security:** Complete all items in `HARDCODED_VALUES_AUDIT.md`
2. **Backend:** Deploy to Google Cloud Run
3. **Frontend:** Deploy to Vercel/Firebase
4. **Database:** Use Cloud SQL or managed TimescaleDB
5. **Secrets:** Use Google Secret Manager
6. **Monitoring:** Set up logging and alerts

---

## 🐛 Troubleshooting

### Backend won't start
- Check database connection (TimescaleDB running?)
- Verify `.env` file exists and has all required variables
- Check Google credentials file exists: `backend/app/services/ee-credentials.json`
- Review logs for specific error messages

### GEE 503 errors
- Verify service account has "Earth Engine Resource Viewer" role
- Check credentials file is valid JSON
- Ensure Earth Engine API is enabled in GCP project

### Frontend can't connect to backend
- Verify `VITE_API_URL` in frontend `.env`
- Check CORS settings in `backend/app/main.py`
- Ensure backend is running on correct port (8080)

### ML predictions are wrong
- Check if model weights file exists
- Verify scaler file is present
- Review input feature scaling
- Check for NaN values in input data

---

## 📊 Performance Tips

### Backend
- Enable Redis caching for API responses
- Use connection pooling for database
- Implement rate limiting
- Cache GEE satellite queries (15-minute TTL)
- Pre-compute ward predictions

### Frontend
- Lazy load map tiles
- Debounce API calls
- Use React.memo for expensive components
- Implement virtual scrolling for large lists
- Cache Supabase queries

---

## 🔒 Security Checklist

- [ ] All API keys in environment variables (not code)
- [ ] Service account files NOT in repository
- [ ] Strong database passwords
- [ ] CORS restricted to specific origins
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (React escapes by default)
- [ ] HTTPS in production
- [ ] Regular dependency updates

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Leaflet Docs:** https://leafletjs.com/
- **TimescaleDB Docs:** https://docs.timescale.com/
- **PyTorch Docs:** https://pytorch.org/docs/

---

## 🆘 Getting Help

1. Check `HARDCODED_VALUES_AUDIT.md` for configuration issues
2. Review `AUDIT_SESSION_LOG.md` for recent changes
3. Search GitHub issues
4. Check service provider status pages
5. Review application logs

---

**Pro Tip:** Keep this document updated as the project evolves!
