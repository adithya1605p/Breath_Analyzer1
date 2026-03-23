# Online Datasets for Air Quality Model Training

**Last Updated:** March 24, 2026  
**Purpose:** Comprehensive guide to online data sources for improving VayuDrishti model accuracy

---

## 🎯 Current Status

- **Current Model Accuracy:** 54-59%
- **Target Accuracy:** 75-80%
- **Current Dataset Size:** 2,007 samples (2015-2020)
- **Target Dataset Size:** 10,000+ samples (2020-2026)

---

## 📊 Recommended Online Datasets

### 1. WAQI (World Air Quality Index) - HIGHEST PRIORITY ⭐⭐⭐⭐⭐

**Why:** Real-time, reliable, already integrated

**API:** https://aqicn.org/api/  
**Cost:** Free (1000 requests/day)  
**Coverage:** 10+ Delhi stations  
**Update Frequency:** Hourly  
**Data Available:** PM2.5, PM10, NO2, SO2, CO, O3, Temperature, Humidity

**How to Use:**
```bash
cd backend
python collect_online_data.py
```

**Pros:**
- Already have API token
- Real-time data
- High quality
- Multiple stations
- Weather data included

**Cons:**
- Rate limited (1000/day)
- Historical data limited to 30 days

**Expected Improvement:** +10-15% accuracy

---

### 2. OpenAQ - HIGH PRIORITY ⭐⭐⭐⭐

**Why:** Large historical dataset, free, reliable

**API:** https://docs.openaq.org/  
**Cost:** Free (unlimited)  
**Coverage:** 50+ Delhi locations  
**Historical Data:** 2015-present  
**Data Available:** PM2.5, PM10, NO2, SO2, CO, O3

**How to Use:**
```python
# Already implemented in collect_online_data.py
python collect_online_data.py
```

**API Example:**
```bash
curl "https://api.openaq.org/v2/measurements?country=IN&city=Delhi&parameter=pm25&date_from=2024-01-01&limit=10000"
```

**Pros:**
- Free unlimited access
- Large historical dataset
- Good coverage
- Well-documented API

**Cons:**
- Some data gaps
- Quality varies by station

**Expected Improvement:** +5-10% accuracy

---

### 3. CPCB (Central Pollution Control Board) - HIGH PRIORITY ⭐⭐⭐⭐

**Why:** Official government data, most authoritative

**Website:** https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing  
**Cost:** Free  
**Coverage:** 40+ Delhi stations  
**Update Frequency:** Hourly  
**Data Available:** PM2.5, PM10, NO2, SO2, CO, O3, NH3

**How to Use:**
1. Visit CPCB portal
2. Select Delhi
3. Download historical data (CSV)
4. Place in `backend/collected_data/cpcb_data.csv`
5. Run `python collect_online_data.py`

**Note:** No public API - requires manual download or web scraping

**Pros:**
- Official government data
- Most authoritative
- Comprehensive coverage
- Free

**Cons:**
- No API (manual download)
- Website can be slow
- Data format inconsistent

**Expected Improvement:** +5-8% accuracy

---

### 4. Sentinel-5P Satellite Data - MEDIUM PRIORITY ⭐⭐⭐

**Why:** Spatial coverage, PM10 correlation

**API:** Google Earth Engine  
**Cost:** Free  
**Coverage:** Entire Delhi region  
**Update Frequency:** Daily  
**Data Available:** NO2, SO2, CO, O3, Aerosol Optical Depth

**How to Use:**
```python
# Already have GEE integration
# See: backend/app/services/gee_satellite.py
```

**Pros:**
- Spatial coverage
- Helps with PM10 prediction
- Already integrated
- Free

**Cons:**
- Requires processing
- Not direct PM measurements
- Cloud cover issues

**Expected Improvement:** +3-5% accuracy (especially for PM10)

---

### 5. IQAir - MEDIUM PRIORITY ⭐⭐⭐

**Why:** High-quality data, good coverage

**API:** https://www.iqair.com/air-pollution-data-api  
**Cost:** Free tier (10,000 calls/month)  
**Coverage:** 5+ Delhi stations  
**Update Frequency:** Real-time  
**Data Available:** PM2.5, PM10, AQI

**API Example:**
```bash
curl "https://api.airvisual.com/v2/city?city=Delhi&state=Delhi&country=India&key=YOUR_KEY"
```

**Pros:**
- High quality
- Real-time
- Good API

**Cons:**
- Limited free tier
- Fewer stations than WAQI

**Expected Improvement:** +2-3% accuracy

---

### 6. Weather Data (OpenWeatherMap) - MEDIUM PRIORITY ⭐⭐⭐

**Why:** Weather strongly correlates with air quality

**API:** https://openweathermap.org/api  
**Cost:** Free (1000 calls/day)  
**Coverage:** Delhi  
**Update Frequency:** Hourly  
**Data Available:** Temperature, Humidity, Wind Speed, Wind Direction, Pressure, Precipitation

**How to Use:**
```python
import requests

api_key = "your_key"
url = f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={api_key}"
response = requests.get(url)
data = response.json()
```

**Pros:**
- Free
- Reliable
- Easy to use
- Historical data available

**Cons:**
- Requires separate API key
- Need to correlate with AQI data

**Expected Improvement:** +5-7% accuracy

---

### 7. NASA POWER - LOW PRIORITY ⭐⭐

**Why:** Long-term climate data

**API:** https://power.larc.nasa.gov/  
**Cost:** Free  
**Coverage:** Global (including Delhi)  
**Historical Data:** 1981-present  
**Data Available:** Solar radiation, Temperature, Humidity, Wind

**Pros:**
- Free
- Long historical data
- Reliable

**Cons:**
- Low spatial resolution
- Not real-time
- Indirect correlation

**Expected Improvement:** +1-2% accuracy

---

## 🚀 Implementation Priority

### Phase 1: Quick Wins (Week 1)
1. **WAQI** - Run `collect_online_data.py` daily for 7 days
2. **OpenAQ** - Fetch last 365 days of data
3. **Weather** - Get OpenWeatherMap API key, collect data

**Expected Dataset Size:** 5,000+ samples  
**Expected Accuracy Improvement:** +15-20%

### Phase 2: Government Data (Week 2)
1. **CPCB** - Manual download of historical data
2. **Sentinel-5P** - Process satellite data for PM10 correlation

**Expected Dataset Size:** 10,000+ samples  
**Expected Accuracy Improvement:** +20-25%

### Phase 3: Additional Sources (Week 3-4)
1. **IQAir** - Get API key, collect data
2. **NASA POWER** - Historical climate data

**Expected Dataset Size:** 15,000+ samples  
**Expected Accuracy Improvement:** +25-30%

---

## 📝 Data Collection Scripts

### Automated Collection (Recommended)

```bash
# Collect from all online sources
cd backend
python collect_online_data.py

# This will create:
# - collected_data/waqi_current.csv
# - collected_data/openaq_historical.csv
# - collected_data/combined_training_data.csv
```

### Manual Collection

#### CPCB Data
1. Visit https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing
2. Select "Delhi" from dropdown
3. Select date range (last 2 years)
4. Click "Download CSV"
5. Save as `backend/collected_data/cpcb_data.csv`

#### Weather Data
```python
import requests
import pandas as pd
from datetime import datetime, timedelta

api_key = "your_openweathermap_key"
lat, lon = 28.6139, 77.2090  # Delhi

# Historical data (requires paid plan)
# Or use free current weather and collect over time
```

---

## 🔧 Data Preprocessing

After collecting data, preprocess it:

```bash
cd backend

# Combine all sources
python collect_online_data.py

# Train with new data
python train_advanced.py
```

The training script will:
1. Load all collected data
2. Clean and preprocess
3. Add temporal features
4. Train multiple model architectures
5. Select best model
6. Save results

---

## 📈 Expected Results

### With Current Data (2,007 samples)
- PM2.5 Accuracy: 54%
- PM10 Accuracy: 59%

### With WAQI + OpenAQ (5,000+ samples)
- PM2.5 Accuracy: 65-70%
- PM10 Accuracy: 70-75%

### With All Sources (10,000+ samples)
- PM2.5 Accuracy: 75-80%
- PM10 Accuracy: 80-85%

### With Advanced Features (15,000+ samples + weather)
- PM2.5 Accuracy: 80-85%
- PM10 Accuracy: 85-90%

---

## 🎓 Best Practices

### 1. Data Quality
- Remove outliers (AQI > 999)
- Handle missing values (forward fill, interpolation)
- Validate against multiple sources

### 2. Data Diversity
- Collect from multiple stations
- Include different seasons
- Include different times of day
- Include weekdays and weekends

### 3. Feature Engineering
- Add temporal features (hour, day, month, season)
- Add spatial features (latitude, longitude, ward)
- Add weather features (temp, humidity, wind)
- Add derived features (PM10/PM2.5 ratio)

### 4. Model Training
- Use train/validation/test split (70/15/15)
- Use cross-validation
- Monitor for overfitting
- Try multiple architectures

---

## 🔗 Useful Links

### APIs
- WAQI: https://aqicn.org/api/
- OpenAQ: https://docs.openaq.org/
- IQAir: https://www.iqair.com/air-pollution-data-api
- OpenWeatherMap: https://openweathermap.org/api
- NASA POWER: https://power.larc.nasa.gov/

### Data Portals
- CPCB: https://app.cpcbccr.com/ccr/
- Delhi Pollution Control Committee: http://www.dpcc.delhigovt.nic.in/
- India Air Quality: https://www.aqi.in/

### Research Papers
- "Air Quality Prediction using Machine Learning" - IEEE
- "PM2.5 and PM10 Prediction using Deep Learning" - Nature
- "Spatial-Temporal Air Quality Forecasting" - ACM

---

## 📞 Support

### API Keys Needed
1. WAQI Token - Already have ✅
2. OpenWeatherMap API Key - Get from https://openweathermap.org/api
3. IQAir API Key (optional) - Get from https://www.iqair.com/

### Troubleshooting

**Problem:** WAQI rate limit exceeded  
**Solution:** Collect data once per hour, not more frequently

**Problem:** OpenAQ returns no data  
**Solution:** Check date range, try different parameters

**Problem:** CPCB website slow  
**Solution:** Download during off-peak hours (night time)

---

## ✅ Checklist

### Before Training
- [ ] Collected WAQI data (7+ days)
- [ ] Collected OpenAQ data (365 days)
- [ ] Downloaded CPCB data (manual)
- [ ] Collected weather data
- [ ] Combined all datasets
- [ ] Preprocessed data
- [ ] Verified data quality

### During Training
- [ ] Run train_advanced.py
- [ ] Monitor training progress
- [ ] Compare multiple architectures
- [ ] Select best model
- [ ] Validate on test set

### After Training
- [ ] Test with test_aqi_validation.py
- [ ] Compare with real WAQI data
- [ ] Document accuracy improvements
- [ ] Deploy to production

---

**Next Steps:**
1. Run `python collect_online_data.py` to start collecting data
2. Wait 7 days for sufficient WAQI data
3. Run `python train_advanced.py` to train improved model
4. Test and deploy

**Questions?** Check the documentation or create an issue on GitHub.
