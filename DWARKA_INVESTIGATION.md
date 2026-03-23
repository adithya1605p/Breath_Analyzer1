# Dwarka Anomaly Investigation

**Location:** Dwarka, Delhi (28.5921, 77.0460)  
**Issue:** 61.3% prediction error (488 real AQI vs 189 predicted)  
**Priority:** HIGH

---

## 🔍 Problem Analysis

### Observed Data (March 24, 2026, 00:00)

**WAQI Real-Time Data:**
- AQI: 488 (Hazardous)
- PM2.5: 142 µg/m³
- PM10: 488 µg/m³ ⚠️ EXTREMELY HIGH
- Station: National Institute of Malaria Research, Sector 8, Dwarka

**VayuDrishti Prediction:**
- AQI: 189 (Unhealthy)
- PM2.5: 128.6 µg/m³
- PM10: Not predicted

### Key Findings

1. **PM2.5 Accuracy: EXCELLENT (9.4% difference)**
   - Real: 142 µg/m³
   - Predicted: 128.6 µg/m³
   - Difference: Only 13.4 µg/m³

2. **PM10 Spike: NOT CAPTURED**
   - Real: 488 µg/m³ (EXTREME)
   - Predicted: None (model doesn't predict PM10)
   - This is the root cause of the AQI mismatch

3. **AQI Calculation:**
   - WAQI AQI is driven by PM10 (488), not PM2.5
   - Our AQI is calculated from PM2.5 only
   - **Conclusion:** Model is accurate for what it predicts, but missing PM10

---

## 🏗️ Why PM10 is High in Dwarka

### Geographic Analysis

**Dwarka Characteristics:**
- Residential area in West Delhi
- Major construction activity (new metro lines, housing projects)
- Industrial zones nearby (Najafgarh industrial area)
- High traffic density (NH 48 highway)
- Dust from unpaved roads

### PM10 Sources in Dwarka

1. **Construction Dust (Primary)**
   - Multiple ongoing construction projects
   - Demolition activities
   - Material transport
   - Unpaved construction sites

2. **Road Dust Resuspension**
   - Heavy vehicle traffic
   - Unpaved roads in some sectors
   - Wind-blown dust

3. **Industrial Emissions**
   - Nearby Najafgarh industrial area
   - Small-scale industries
   - Brick kilns

4. **Seasonal Factors**
   - March is pre-monsoon (dry season)
   - High wind speeds
   - Low humidity
   - Increased dust suspension

### Temporal Patterns

**When PM10 Spikes Occur:**
- Morning rush hour (7-10 AM)
- Evening rush hour (5-8 PM)
- Windy days
- Dry season (March-May)
- Construction working hours

---

## 📊 Data Collection Plan

### Step 1: Collect Dwarka-Specific Data

```python
# File: backend/scripts/collect_dwarka_data.py

import requests
import pandas as pd
from datetime import datetime, timedelta

WAQI_TOKEN = "9abbe99f4595fa8a4d20dd26a06db8e375273034"
DWARKA_LAT = 28.5921
DWARKA_LON = 77.0460

def collect_dwarka_hourly(days=30):
    """Collect hourly data for Dwarka for 30 days"""
    
    data = []
    
    for day in range(days):
        for hour in range(24):
            # Fetch data
            url = f"https://api.waqi.info/feed/geo:{DWARKA_LAT};{DWARKA_LON}/"
            response = requests.get(url, params={"token": WAQI_TOKEN})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "ok":
                    d = result.get("data", {})
                    iaqi = d.get("iaqi", {})
                    
                    data.append({
                        "timestamp": datetime.now() - timedelta(days=day, hours=hour),
                        "aqi": d.get("aqi"),
                        "pm25": iaqi.get("pm25", {}).get("v"),
                        "pm10": iaqi.get("pm10", {}).get("v"),
                        "no2": iaqi.get("no2", {}).get("v"),
                        "so2": iaqi.get("so2", {}).get("v"),
                        "co": iaqi.get("co", {}).get("v"),
                        "temp": iaqi.get("t", {}).get("v"),
                        "humidity": iaqi.get("h", {}).get("v"),
                        "wind_speed": iaqi.get("w", {}).get("v"),
                    })
            
            time.sleep(3600)  # Wait 1 hour
    
    df = pd.DataFrame(data)
    df.to_csv('dwarka_30days.csv', index=False)
    return df
```

### Step 2: Analyze Patterns

```python
# File: backend/scripts/analyze_dwarka.py

import pandas as pd
import matplotlib.pyplot as plt

def analyze_dwarka_patterns():
    """Analyze Dwarka PM10 patterns"""
    
    df = pd.read_csv('dwarka_30days.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # 1. Hourly pattern
    hourly_avg = df.groupby('hour')[['pm25', 'pm10']].mean()
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(hourly_avg.index, hourly_avg['pm25'], label='PM2.5')
    plt.plot(hourly_avg.index, hourly_avg['pm10'], label='PM10')
    plt.xlabel('Hour of Day')
    plt.ylabel('Concentration (µg/m³)')
    plt.title('Dwarka: Hourly Pollution Pattern')
    plt.legend()
    plt.grid(True)
    
    # 2. PM10/PM2.5 ratio
    df['pm10_pm25_ratio'] = df['pm10'] / df['pm25']
    
    plt.subplot(1, 2, 2)
    plt.hist(df['pm10_pm25_ratio'].dropna(), bins=30)
    plt.xlabel('PM10/PM2.5 Ratio')
    plt.ylabel('Frequency')
    plt.title('Dwarka: PM10/PM2.5 Ratio Distribution')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('dwarka_analysis.png')
    
    # Statistics
    print("Dwarka PM10 Statistics:")
    print(f"  Mean PM10: {df['pm10'].mean():.1f} µg/m³")
    print(f"  Max PM10: {df['pm10'].max():.1f} µg/m³")
    print(f"  PM10 > 200 (High): {(df['pm10'] > 200).sum()} hours ({(df['pm10'] > 200).sum()/len(df)*100:.1f}%)")
    print(f"  PM10 > 400 (Extreme): {(df['pm10'] > 400).sum()} hours ({(df['pm10'] > 400).sum()/len(df)*100:.1f}%)")
    print(f"\n  Mean PM10/PM2.5 Ratio: {df['pm10_pm25_ratio'].mean():.2f}")
    print(f"  Typical ratio: 1.5-2.0 (normal)")
    print(f"  Dwarka ratio: {df['pm10_pm25_ratio'].mean():.2f} (construction/dust impact)")
```

---

## 🔧 Solution Implementation

### Solution 1: Add PM10 Prediction (RECOMMENDED)

**Already covered in STEP_BY_STEP_TRAINING_GUIDE.md**

Key points:
- Train dual-output model (PM2.5 + PM10)
- Use PM10/PM2.5 ratio as feature
- Add construction zone indicator
- Include wind speed (affects dust resuspension)

### Solution 2: Add Construction Zone Features

```python
# File: backend/app/services/construction_zones.py

CONSTRUCTION_ZONES = {
    "dwarka": {
        "center": (28.5921, 77.0460),
        "radius_km": 5,
        "pm10_multiplier": 1.8,  # PM10 is 80% higher in construction zones
        "active_since": "2024-01-01",
        "projects": [
            "Dwarka Metro Extension",
            "Dwarka Expressway",
            "Housing Projects Sector 23-28"
        ]
    },
    "rohini": {
        "center": (28.7041, 77.1025),
        "radius_km": 3,
        "pm10_multiplier": 1.5,
        "active_since": "2025-06-01",
        "projects": ["Rohini Metro Station Upgrade"]
    }
}

def is_in_construction_zone(lat, lon):
    """Check if location is in active construction zone"""
    import math
    
    for zone_name, zone_data in CONSTRUCTION_ZONES.items():
        center_lat, center_lon = zone_data["center"]
        radius_km = zone_data["radius_km"]
        
        # Calculate distance
        dist_km = math.sqrt(
            (lat - center_lat)**2 + (lon - center_lon)**2
        ) * 111  # Rough km conversion
        
        if dist_km <= radius_km:
            return True, zone_data["pm10_multiplier"]
    
    return False, 1.0

def adjust_pm10_for_construction(pm10_base, lat, lon):
    """Adjust PM10 prediction for construction zones"""
    in_zone, multiplier = is_in_construction_zone(lat, lon)
    
    if in_zone:
        return pm10_base * multiplier
    return pm10_base
```

### Solution 3: Real-Time Calibration

```python
# File: backend/app/services/realtime_calibration.py

import requests
from datetime import datetime, timedelta

class RealtimeCalibrator:
    """Calibrate predictions using recent WAQI data"""
    
    def __init__(self):
        self.calibration_cache = {}
        self.cache_duration = timedelta(hours=1)
    
    def get_calibration_factor(self, lat, lon):
        """Get calibration factor for location"""
        
        cache_key = f"{lat:.4f},{lon:.4f}"
        
        # Check cache
        if cache_key in self.calibration_cache:
            cached_time, factor = self.calibration_cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return factor
        
        # Fetch recent WAQI data
        try:
            url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
            response = requests.get(url, params={"token": WAQI_TOKEN}, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    real_pm10 = data.get("data", {}).get("iaqi", {}).get("pm10", {}).get("v")
                    real_pm25 = data.get("data", {}).get("iaqi", {}).get("pm25", {}).get("v")
                    
                    if real_pm10 and real_pm25:
                        # Calculate PM10/PM2.5 ratio
                        ratio = real_pm10 / real_pm25
                        
                        # Cache it
                        self.calibration_cache[cache_key] = (datetime.now(), ratio)
                        return ratio
        except:
            pass
        
        return 1.5  # Default ratio
    
    def calibrate_prediction(self, pm25_pred, lat, lon):
        """Calibrate PM10 prediction using real-time ratio"""
        
        ratio = self.get_calibration_factor(lat, lon)
        pm10_pred = pm25_pred * ratio
        
        return pm10_pred
```

---

## ✅ Validation Plan

### Test Cases for Dwarka

1. **Normal Conditions**
   - Expected: PM10/PM2.5 ratio ~1.5
   - Model should predict both accurately

2. **Construction Hours (9 AM - 5 PM)**
   - Expected: PM10/PM2.5 ratio ~2.0-2.5
   - Model should apply construction multiplier

3. **Windy Days**
   - Expected: Higher PM10 due to dust resuspension
   - Model should factor in wind speed

4. **Evening Rush Hour**
   - Expected: PM10 spike from traffic
   - Model should capture temporal pattern

### Success Criteria

- Dwarka AQI accuracy: < 20% difference
- PM10 prediction: < 30% difference
- PM10/PM2.5 ratio: Within 0.5 of actual

---

## 📈 Expected Improvements

**Before:**
- Dwarka AQI difference: 61.3%
- PM10 detection: ❌ None

**After:**
- Dwarka AQI difference: < 20%
- PM10 detection: ✅ Working
- Construction zone handling: ✅ Implemented
- Real-time calibration: ✅ Active

---

**Status:** Ready for implementation  
**Priority:** HIGH  
**Timeline:** 1 week
