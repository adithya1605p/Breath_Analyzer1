# VayuDrishti Hardcoded Values Audit

**Last Updated:** March 23, 2026  
**Purpose:** Track all hardcoded values, credentials, and configuration that should be externalized

---

## 🚨 CRITICAL SECURITY ISSUES

### Exposed API Keys & Credentials

#### Backend Environment Files
**File:** `backend/.env`
- ⚠️ **WAQI_TOKEN:** `9abbe99f4595fa8a4d20dd26a06db8e375273034` (Air Quality API)
- ⚠️ **GCP_PROJECT_ID:** `gee-data-490807`
- ⚠️ **VITE_SUPABASE_URL:** `https://tmavkmymbdcmugunjtle.supabase.co`
- ⚠️ **VITE_SUPABASE_ANON_KEY:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (JWT token)

**File:** `web-frontend/.env.local`
- ⚠️ Same Supabase credentials as above
- ⚠️ **VITE_API_URL:** `http://localhost:8080`

**File:** `web-frontend/.env`
- ⚠️ **VITE_API_URL:** `http://192.168.0.137:8080` (Local network IP)

#### Service Account Files (CONTAINS PRIVATE KEYS)
- `backend/app/services/ee-credentials.json` - Google Earth Engine service account
- `backend/app/services/gee-data-490807-df45431ef2de.json` - GCP credentials
- `backend/scripts/ee-credentials.json.json` - Duplicate credentials

**Action Required:** Move all credentials to secure secret management (Google Secret Manager, AWS Secrets Manager, or environment-only variables)

---

## 📍 GEOGRAPHIC & LOCATION HARDCODES

### Delhi Bounding Boxes
**File:** `backend/app/api/endpoints/dashboard.py`
- Delhi NCR bounds: `[28.4, 76.8, 28.9, 77.4]` (lat/lon)
- WAQI API URL: `https://api.waqi.info/map/bounds/?latlng=28.4,76.8,28.9,77.4&token={WAQI_TOKEN}`

**File:** `backend/app/services/gee_satellite.py`
- Delhi bounds: `[76.84, 28.40, 77.34, 28.88]`

**File:** `backend/app/services/ml_engine.py`
- Delhi city center: `(28.6139, 77.2090)`
- Distance calculation reference: `(28.61, 77.20)`

**File:** `backend/app/services/cpcb_sensors.py`
- Default location: `lat=28.6139, lon=77.2090`
- Default radius: `25000` meters (25km)

### Hyderabad Routing
**File:** `backend/app/api/endpoints/navigation.py`
- Hyderabad center: `(17.4239, 78.4738)`
- Map radius: `8000` meters (8km)
- Max snap distance: `8000` meters
- Cached graph file: `hyderabad_cached.graphml`

**Recommendation:** Create a city configuration system with JSON/YAML files for each supported city

---

## 🗄️ DATABASE HARDCODES

### Connection Defaults
**File:** `backend/app/core/config.py`
```python
POSTGRES_SERVER: str = "localhost"
POSTGRES_USER: str = "postgres"
POSTGRES_PASSWORD: str = "postgres"
POSTGRES_DB: str = "breath_analyzer"
POSTGRES_PORT: int = 5432
```

**File:** `backend/docker-compose.yml`
```yaml
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=breath_analyzer
```

**File:** `backend/app/db/database.py`
- Echo mode: `echo=True` (Should be False in production)

**Recommendation:** Use strong passwords and environment variables for all database credentials

---

## 🤖 AI/ML MODEL HARDCODES

### Model File Paths
**File:** `backend/app/ai/inference.py`
- Weights path: `backend/app/data/a3tgcn_weights.pt`
- Training data: `backend/app/data/synthetic_training_tensor.pkl`
- Graph file: `backend/app/data/hyderabad_60km_major.graphml`

**File:** `backend/app/services/ml_engine.py`
- Production model: `vayu_spatial_PRODUCTION.pt`
- Scaler file: `vayu_scaler.pkl`
- Fallback wind vector: `wind_vector_x = 0.8`, `wind_vector_y = 0.4`

### Model Parameters
**File:** `backend/app/ai/inference.py`
- Node features: `5`
- Hidden dimension: `64`
- Sequence length: `24` (hours)
- Baseline city pollution: `45.0` PM2.5

**File:** `backend/app/services/ml_engine.py`
- Neural network architecture:
  - Input: `7` features
  - Layers: `256 → 128 → 64 → 1`
  - Dropout: `0.25`, `0.15`
  - Activation: `SiLU`

### Pollution Emission Profiles (Hardcoded)
**File:** `backend/app/ai/inference.py`
```python
'motorway': +110.0 PM2.5
'primary': +75.0 PM2.5
'secondary': +40.0 PM2.5
'tertiary': +20.0 PM2.5
'residential': -10.0 PM2.5
'pedestrian': -15.0 PM2.5
```

**Recommendation:** Load model paths and parameters from configuration files

---

## 🌐 EXTERNAL API ENDPOINTS

### Hardcoded API URLs
**File:** `backend/app/api/endpoints/dashboard.py`
- WAQI: `https://api.waqi.info/map/bounds/`
- WAQI Feed: `https://api.waqi.info/feed/geo:`

**File:** `backend/app/services/cpcb_sensors.py`
- OpenAQ: `https://api.openaq.org/v3`
- Hardcoded API key in test: `a48c3556e253887d4098147a13ff033b81ccd7ac36fede20ff5c3b8eb7be4029`

**File:** `web-frontend/src/App.tsx`
- API base fallback: `http://127.0.0.1:8080`
- Open-Meteo: `https://air-quality-api.open-meteo.com/v1/air-quality`

**File:** `web-frontend/src/supabaseClient.ts`
- Placeholder URL: `https://placeholder.supabase.co`

---

## ⚙️ CONFIGURATION HARDCODES

### CORS Settings
**File:** `backend/app/main.py`
- Default CORS: `["*"]` (Allow all origins if not configured)
- Credentials path: `backend/app/services/ee-credentials.json`

### Celery/Redis
**File:** `backend/app/core/celery_app.py`
- Broker URL: `redis://localhost:6379/0`
- Task serializer: `json`
- Timezone: `UTC`

### GCP Configuration
**File:** `backend/app/api/endpoints/dashboard.py`
- Default location: `us-central1`
- Project auto-detection from: `ee-credentials.json`

**File:** `backend/app/api/endpoints/gee.py`
- Default location: `us-central1`
- OAuth scopes: `https://www.googleapis.com/auth/earthengine`

---

## 📊 AQI CALCULATION HARDCODES

### US EPA Breakpoints
**File:** `backend/app/services/ml_engine.py`
```python
(0.0,   12.0,  0,   50)    # Good
(12.1,  35.4,  51,  100)   # Moderate
(35.5,  55.4,  101, 150)   # Unhealthy for Sensitive Groups
(55.5,  150.4, 151, 200)   # Unhealthy
(150.5, 250.4, 201, 300)   # Very Unhealthy
(250.5, 350.4, 301, 400)   # Hazardous
(350.5, 500.4, 401, 500)   # Hazardous+
```

**File:** `backend/app/api/endpoints/dashboard.py`
- Same breakpoints duplicated

**Recommendation:** Create a shared AQI utility module to avoid duplication

---

## 🏥 HEALTH CALCULATION HARDCODES

### Safe Exposure Calculations
**File:** `backend/app/api/endpoints/users.py`
- Baseline safe time: `1440` minutes (24 hours at AQI 50)
- Asthma reduction: `40%` (0.6 multiplier)
- Age threshold: `65` years (elderly)
- Age threshold: `12` years (children)
- Age-based reduction: `50%` (0.5 multiplier)
- AQI danger threshold: `200`

---

## 🛰️ SATELLITE DATA HARDCODES

### Google Earth Engine
**File:** `backend/app/api/endpoints/gee.py`
- Sentinel-5P collections:
  - `COPERNICUS/S5P/NRTI/L3_AER_AI` (Aerosol Index)
  - `COPERNICUS/S5P/NRTI/L3_CO` (Carbon Monoxide)
- Date range: `2024-01-01` to `2025-12-31`
- Resolution: `1113.2` meters
- Aerosol threshold: `0.5` UVAI (construction dust)
- CO threshold: `0.04` mol/m² (biomass burning)

**File:** `backend/app/services/gee_satellite.py`
- Same Sentinel-5P collections
- Lookback period: `7` days

---

## 🚗 ROUTING ENGINE HARDCODES

### A* Algorithm Parameters
**File:** `backend/app/services/routing_engine.py`
- Walking speed: `1.4` m/s (5 km/h)
- Minimum theoretical PM2.5: `5.0` µg/m³
- Default alpha (distance weight): `1.0`
- Default beta (health weight): `0.5`
- Earth radius: `6371000` meters

**File:** `backend/app/api/endpoints/navigation.py`
- Health sensitivity range: `0-100`
- Beta conversion: `health_sensitivity / 100.0`
- Default edge length: `10.0` meters
- Default aspect ratio: `0.8`
- Default sky view factor: `0.5`

---

## 🎨 FRONTEND HARDCODES

### Timeouts & Polling
**File:** `web-frontend/src/App.tsx`
- GEE timeout: `15000` ms (15 seconds)
- Forecast timeout: `8000` ms (8 seconds)
- Supabase timeout: `10000` ms (10 seconds)
- Open-Meteo timeout: `30000` ms (30 seconds)
- Polling interval: `60000` ms (60 seconds)

### UI Configuration
- Ward tier count: `272`
- District tier count: `11`
- Forecast days: `8`
- Wind grid dimensions: `10x10`

---

## 📁 FILE PATH HARDCODES

### GeoJSON Data Files
**File:** `backend/app/api/endpoints/dashboard.py`
- `web-frontend/public/kaggle_wards.geojson`
- `web-frontend/public/delhi_wards.geojson`

### Cache Directories
- `backend/cache/` - 136 JSON cache files
- `backend/app/data/` - Model weights and graph files
- `backend/dataset_extracted/` - CSV datasets

---

## 🔧 DOCKER HARDCODES

**File:** `backend/docker-compose.yml`
- Image: `timescale/timescaledb-ha:pg14-latest`
- Container name: `breath_analyzer_db`
- Port mapping: `5432:5432`
- Volume: `timescale_data:/home/postgres/pgdata/data`
- Init script: `./app/db/init.sql`
- Shared libraries: `timescaledb`

---

## 📝 RECOMMENDATIONS

### Immediate Actions
1. **Move all credentials to environment variables** - Never commit `.env` files
2. **Use Secret Manager** - Google Secret Manager or AWS Secrets Manager for production
3. **Rotate exposed API keys** - WAQI token and Supabase keys are publicly visible
4. **Remove service account JSON files from repo** - Use workload identity or mounted secrets
5. **Create `.env.template`** - With placeholder values only

### Configuration Improvements
1. **City configuration system** - JSON/YAML files for each supported city
2. **Centralized AQI calculations** - Single source of truth for breakpoints
3. **Model registry** - Track model versions and paths in database
4. **Feature flags** - Enable/disable features without code changes
5. **API endpoint configuration** - External service URLs in config files

### Code Quality
1. **Remove duplicate code** - AQI calculations appear in multiple files
2. **Consolidate constants** - Create `constants.py` modules
3. **Type safety** - Use TypedDict or Pydantic for all configuration
4. **Validation** - Validate all configuration on startup
5. **Documentation** - Document all configuration options

---

## 📋 CHANGE LOG

### March 23, 2026 - Initial Audit
- Identified 150+ hardcoded values across backend and frontend
- Found exposed credentials in `.env` files
- Documented all geographic, model, and API hardcodes
- Created recommendations for externalization

---

**Next Steps:** Review this document with the team and prioritize security fixes before deployment.
