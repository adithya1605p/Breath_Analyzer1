# 🌍 VayuDrishti: Atmospheric Command System

VayuDrishti is an **Enterprise-Grade Air Quality Intelligence & Predictive Dashboard** built for hyper-local environmental monitoring in Delhi. It aggregates real-time monitoring stations, satellite telemetry, and meteorological data into a seamless React-based spatial command center.

The core objective is to provide actionable municipal insights—shifting from purely displaying current AQI to actively predicting pollution trajectories and generating immediate policy enforcement directives using Google Cloud's most advanced experimental AI models.

---

## 📚 Documentation

### Analysis & Testing
- **[📋 Executive Summary](./CODEBASE_ANALYSIS_SUMMARY.md)** - High-level overview of analysis and findings
- **[🚀 Quick Reference Guide](./QUICK_REFERENCE.md)** - Setup, API endpoints, common tasks
- **[🔒 Hardcoded Values Audit](./HARDCODED_VALUES_AUDIT.md)** - Security audit and configuration tracking
- **[📝 Audit Session Log](./AUDIT_SESSION_LOG.md)** - Detailed analysis and findings
- **[🧪 Testing Summary](./TESTING_SUMMARY.md)** - End-to-end test results overview
- **[📊 Test Results Report](./TEST_RESULTS_REPORT.md)** - Comprehensive AQI validation analysis

### Improvement Roadmap
- **[🎯 Action Plan](./ACTION_PLAN.md)** - 4-week step-by-step implementation plan
- **[📖 Step-by-Step Training Guide](./STEP_BY_STEP_TRAINING_GUIDE.md)** - Complete model retraining instructions
- **[🔍 Dwarka Investigation](./DWARKA_INVESTIGATION.md)** - Detailed analysis of Dwarka anomaly
- **[✨ New Features Report](./NEW_FEATURES_REPORT.md)** - Recommended features and improvements
- **[🗺️ Improvement Roadmap](./IMPROVEMENT_ROADMAP.md)** - Long-term enhancement strategy

---

## 🚀 What We Accomplished
Throughout the development journey, we transformed a prototype dashboard into a hardened, production-ready system:

1. **Full-Stack Architecture**: Stabilized a **FastAPI/PyTorch backend** mapped to a **Vite + React (Tailwind/Leaflet) frontend**, authenticated entirely via **Supabase**.
2. **Neural Forecasting (TNN)**: Trained and integrated a custom predictive Temporal Neural Network (`train_vayu_v2.py`) based on real, historical Delhi AQI indices (251 distinct geographic wards) instead of relying purely on generalized third-party APIs.
3. **Admin Enforcement Suite**: Deployed a fully secured Admin portal allowing specialized municipal actions (assigning tasks, evaluating complaints). Resolved dangerous JWT token handling bugs within `deps.py` that caused infinite 401 Unauthorized loops.
4. **Google Earth Engine Integration**: Successfully linked the system to Sentinel-5P satellite telemetry (`gee.py`). Replaced unsafe hardcoded keys with a secure OAuth2 cryptographically signed Service Account method (`ee-credentials.json`).
5. **Experimental AI (Gemini 3 Pro Preview)**: Replaced mock recommendation logic with live, unreleased Vertex AI model inference via Model Garden, generating actual policy reactions based on incoming satellite and terrestrial data.
6. **Local Network Broadcasting**: Configured the Vite frontend and FastAPI CORS middleware dynamically so the mobile-responsive interface could be accessed and demoed natively across internal Wi-Fi networks (e.g., `192.168.0.137`) for live phone testing.

---

## 🛑 Challenges Faced & Resolved

* **Vertex AI Model Garden 404s**:
  * **Issue**: The API consistently threw `NOT_FOUND` on the `gemini-3-pro-preview` model despite it being explicitly linked by Google Cloud.
  * **Fix**: Discovered that experimental Model Garden instances bypass standard API routing. We fundamentally reprogrammed the `google-genai` SDK logic to target explicitly the `global` region flag, successfully bypassing the default `us-central1` rejections.

* **Earth Engine Initialization Crashes**:
  * **Issue**: Even after replacing API keys with a correct Service Account JSON file, the Google Earth Engine Python API crashed the server on boot natively with `503` and gRPC errors.
  * **Fix**: It wasn't enough to enable the Earth Engine API at a project level. We diagnosed the underlying IAM tree and realized the Service Account specifically required the `Earth Engine Resource Viewer` role attached to it in Google Cloud Console. Guided the deployment through this final authentication barrier.

* **Frontend Flexbox Clipping (CSS CSS Bug)**:
  * **Issue**: The newly activated "Orbital Analysis" block loaded satellite data perfectly from backend but was viciously crushed to `0px` inside the Right Nav Panel.
  * **Fix**: The massive flex-box requirements of the 8-Day Neural Forecast chart on smaller laptop screens forcibly collapsed adjacent UI elements. Reprogrammed the DOM with absolute `shrink-0` bounds to prevent React from legally prioritizing chart space over critical telemetry.

---

## 📋 Configuration & Security Audit

**IMPORTANT**: A comprehensive audit of hardcoded values has been documented in [`HARDCODED_VALUES_AUDIT.md`](./HARDCODED_VALUES_AUDIT.md).

This audit identifies:
- 🚨 Exposed API keys and credentials that need immediate rotation
- 📍 Geographic hardcodes (Delhi/Hyderabad boundaries, coordinates)
- 🗄️ Database configuration defaults
- 🤖 AI/ML model paths and parameters
- 🌐 External API endpoints
- 🏥 Health calculation thresholds
- 🛰️ Satellite data collection parameters

**Action Required Before Production Deployment:**
1. Rotate all exposed API keys (WAQI, Supabase)
2. Move credentials to Google Secret Manager
3. Remove service account JSON files from repository
4. Externalize all configuration to environment variables
5. Review and implement security recommendations

---

## ⏭️ What Happens Next?

With the system secured under "enterprise lock-down" (zero mock data, full live API streams), the immediate next phases are:

1. **Security Hardening**: Address all items in `HARDCODED_VALUES_AUDIT.md` before deployment
2. **Public Cloud Deployment**: Containerize the FastAPI backend via **Docker** and push to **Google Cloud Run** using the existing `gee-data-490807` infrastructure. Host the React frontend on **Vercel** or **Firebase Hosting**.
3. **Continuous AI Fine-Tuning**: Now that Gemini 3 is ingesting dynamic satellite payloads, we can feed it specialized municipal handbooks through Vertex AI's context engine to produce specifically formulated legal mandates rather than general mitigation strategies.
4. **WebSockets for Live Refresh**: Upgrade the current REST-based fetching strategy on the frontend maps to an active WebSocket listener, automatically re-rendering the satellite layers the second a sudden PM2.5 anomaly spikes.
5. **Push Notifications Flow**: Finalize the Supabase Edge Functions required to instantly text/email administrative users when an Admin Action is triggered by the system.
