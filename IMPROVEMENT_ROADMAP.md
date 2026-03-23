# VayuDrishti Improvement Roadmap

**Created:** March 24, 2026  
**Priority:** HIGH  
**Timeline:** 4 weeks

---

## 🎯 Overview

This document provides step-by-step instructions to improve VayuDrishti's accuracy from 69.5% to 85%+ and add critical missing features.

---

## 📊 Current Status vs Target

| Metric | Current | Target (4 weeks) |
|--------|---------|------------------|
| Average AQI Accuracy | 69.5% | 85% |
| Central Delhi Accuracy | 91.5% | 95% |
| Industrial Area Accuracy | 62% | 80% |
| PM10 Detection | ❌ None | ✅ Implemented |
| Model Freshness | Unknown | 2026 data |
| API Endpoints Working | 60% | 100% |

---

## 🚨 Phase 1: Critical Fixes (Week 1)

### Priority 1.1: Investigate Dwarka Anomaly

**Problem:** 61.3% difference (488 real AQI vs 189 predicted)

**Root Cause Analysis:**
- WAQI AQI = 488 (driven by PM10)
- WAQI PM2.5 = 142 µg/m³
- Our PM2.5 = 128.6 µg/m³ (only 9.4% off!)
- **Conclusion:** Model is accurate for PM2.5 but doesn't predict PM10

**Action Items:**


1. **Collect PM10 Data**
   ```python
   # Add to data collection script
   # File: backend/scripts/collect_historical_data.py
   
   import requests
   import pandas as pd
   from datetime import datetime, timedelta
   
   def fetch_waqi_historical_pm10(lat, lon, days=365):
       """Fetch historical PM10 data from WAQI"""
       data = []
       for i in range(days):
           date = datetime.now() - timedelta(days=i)
           # WAQI API call
           response = requests.get(
               f"https://api.waqi.info/feed/geo:{lat};{lon}/",
               params={"token": WAQI_TOKEN}
           )
           if response.status_code == 200:
               result = response.json()
               if result.get("status") == "ok":
                   data_point = result.get("data", {})
                   pm10 = data_point.get("iaqi", {}).get("pm10", {}).get("v")
                   pm25 = data_point.get("iaqi", {}).get("pm25", {}).get("v")
                   if pm10 and pm25:
                       data.append({
                           "date": date,
                           "lat": lat,
                           "lon": lon,
                           "pm10": pm10,
                           "pm25": pm25,
                           "aqi": data_point.get("aqi")
                       })
       return pd.DataFrame(data)
   ```

2. **Analyze Dwarka Patterns**
   - Check if PM10 spikes are common in Dwarka
   - Identify temporal patterns (time of day, day of week)
   - Look for construction/industrial activity correlation

3. **Update Model to Predict PM10**
   - Modify model architecture to output both PM2.5 and PM10
   - Train dual-output model

---

### Priority 1.2: Fix API Endpoints

**Broken Endpoints:**
1. `/api/v1/dashboard/forecast` - Response format error
2. `/api/v1/navigation/route` - 404 Not Found
3. `/api/v1/gee/analyze` - Timeout issues

**Fix Instructions:**

#### Fix Forecast Endpoint
