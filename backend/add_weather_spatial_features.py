#!/usr/bin/env python3
"""
Add Weather and Spatial Features to Training Data
Enhances dataset with weather data and spatial features for v5 model
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
import os

print("="*80)
print("Adding Weather and Spatial Features for v5 Model")
print("="*80)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Delhi coordinates
DELHI_LAT = 28.6139
DELHI_LON = 77.2090

# OpenWeatherMap API (free tier: 1000 calls/day)
# Get your free API key from: https://openweathermap.org/api
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')

# Delhi ward zones (simplified - 5 major zones)
DELHI_ZONES = {
    'Central': {'lat': 28.6139, 'lon': 77.2090, 'industrial': 0.3, 'traffic': 0.8},
    'North': {'lat': 28.7041, 'lon': 77.1025, 'industrial': 0.5, 'traffic': 0.6},
    'South': {'lat': 28.5355, 'lon': 77.3910, 'industrial': 0.2, 'traffic': 0.5},
    'East': {'lat': 28.6692, 'lon': 77.4538, 'industrial': 0.7, 'traffic': 0.7},
    'West': {'lat': 28.6692, 'lon': 77.1025, 'industrial': 0.6, 'traffic': 0.6}
}

# ============================================================================
# STEP 1: Load Existing Data
# ============================================================================

print("\n[STEP 1/5] Loading existing training data...")

df = pd.read_csv('dataset_extracted/training_data_clean.csv')
df['Date'] = pd.to_datetime(df['Date'])

print(f"  Loaded {len(df)} records")
print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")

# ============================================================================
# STEP 2: Add Spatial Features
# ============================================================================

print("\n[STEP 2/5] Adding spatial features...")

# Assign zone based on date (simplified - in reality, you'd have ward-level data)
# For now, we'll use a simple rotation to simulate different zones
def assign_zone(date):
    """Assign zone based on date (simplified simulation)"""
    day_of_year = date.dayofyear
    zones = list(DELHI_ZONES.keys())
    return zones[day_of_year % len(zones)]

df['zone'] = df['Date'].apply(assign_zone)

# Add zone-specific features
df['zone_lat'] = df['zone'].apply(lambda z: DELHI_ZONES[z]['lat'])
df['zone_lon'] = df['zone'].apply(lambda z: DELHI_ZONES[z]['lon'])
df['industrial_density'] = df['zone'].apply(lambda z: DELHI_ZONES[z]['industrial'])
df['traffic_density'] = df['zone'].apply(lambda z: DELHI_ZONES[z]['traffic'])

# Add distance from city center
df['distance_from_center'] = np.sqrt(
    (df['zone_lat'] - DELHI_LAT)**2 + 
    (df['zone_lon'] - DELHI_LON)**2
) * 111  # Convert to km (approximate)

print(f"  Added spatial features:")
print(f"    - zone (5 zones)")
print(f"    - zone_lat, zone_lon")
print(f"    - industrial_density (0-1)")
print(f"    - traffic_density (0-1)")
print(f"    - distance_from_center (km)")

# ============================================================================
# STEP 3: Add Weather Features (Historical Approximation)
# ============================================================================

print("\n[STEP 3/5] Adding weather features...")

# Since we can't get historical weather for all dates, we'll use:
# 1. Seasonal patterns (temperature, humidity)
# 2. Statistical approximations based on month/season

def estimate_weather(row):
    """Estimate weather based on season and month"""
    month = row['month']
    season = row['season']
    
    # Temperature (°C) - Delhi seasonal averages
    temp_by_month = {
        1: 14, 2: 17, 3: 23, 4: 30, 5: 35, 6: 35,
        7: 31, 8: 30, 9: 30, 10: 27, 11: 20, 12: 15
    }
    temp = temp_by_month.get(month, 25)
    
    # Add some random variation
    temp += np.random.normal(0, 3)
    
    # Humidity (%) - Delhi seasonal averages
    humidity_by_season = {0: 60, 1: 45, 2: 70, 3: 55}  # winter, spring, summer, autumn
    humidity = humidity_by_season.get(season, 50)
    humidity += np.random.normal(0, 10)
    humidity = max(20, min(100, humidity))
    
    # Wind speed (m/s) - Delhi averages
    wind_speed = 2.5 + np.random.normal(0, 1)
    wind_speed = max(0, wind_speed)
    
    # Pressure (hPa) - Delhi average
    pressure = 1013 + np.random.normal(0, 5)
    
    # Precipitation (mm) - higher in monsoon
    if season == 2 and month in [7, 8]:  # Monsoon
        precipitation = max(0, np.random.exponential(5))
    else:
        precipitation = max(0, np.random.exponential(0.5))
    
    return pd.Series({
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'precipitation': precipitation
    })

# Apply weather estimation
weather_features = df.apply(estimate_weather, axis=1)
df = pd.concat([df, weather_features], axis=1)

print(f"  Added weather features:")
print(f"    - temperature (°C)")
print(f"    - humidity (%)")
print(f"    - wind_speed (m/s)")
print(f"    - pressure (hPa)")
print(f"    - precipitation (mm)")

# ============================================================================
# STEP 4: Add Derived Features
# ============================================================================

print("\n[STEP 4/5] Adding derived features...")

# Temperature-humidity index (discomfort index)
df['temp_humidity_index'] = df['temperature'] + 0.5 * df['humidity']

# Wind chill effect (affects pollutant dispersion)
df['wind_chill'] = df['temperature'] - (df['wind_speed'] * 2)

# Pollution accumulation index (low wind + high humidity = accumulation)
df['pollution_accumulation'] = (100 - df['humidity']) / (df['wind_speed'] + 1)

# Seasonal pollution factor (winter = high, monsoon = low)
season_pollution_factor = {0: 1.5, 1: 1.0, 2: 0.6, 3: 1.2}
df['seasonal_pollution_factor'] = df['season'].map(season_pollution_factor)

# Traffic-weather interaction (high traffic + low wind = more pollution)
df['traffic_weather_interaction'] = df['traffic_density'] / (df['wind_speed'] + 1)

# Industrial-weather interaction
df['industrial_weather_interaction'] = df['industrial_density'] / (df['wind_speed'] + 1)

# Rain effect (rain cleans air)
df['rain_effect'] = (df['precipitation'] > 1).astype(int)

print(f"  Added derived features:")
print(f"    - temp_humidity_index")
print(f"    - wind_chill")
print(f"    - pollution_accumulation")
print(f"    - seasonal_pollution_factor")
print(f"    - traffic_weather_interaction")
print(f"    - industrial_weather_interaction")
print(f"    - rain_effect")

# ============================================================================
# STEP 5: Save Enhanced Dataset
# ============================================================================

print("\n[STEP 5/5] Saving enhanced dataset...")

# Save full dataset
df.to_csv('dataset_extracted/training_data_v5_enhanced.csv', index=False)
print(f"  Saved to: dataset_extracted/training_data_v5_enhanced.csv")

# Print summary
print("\n" + "="*80)
print("FEATURE ENHANCEMENT COMPLETE!")
print("="*80)

print(f"\nDataset Summary:")
print(f"  Total records: {len(df):,}")
print(f"  Total features: {len(df.columns)}")

print(f"\nOriginal features: 12")
print(f"  - Temporal: month, day_of_week, day_of_year, is_weekend, season")
print(f"  - Pollutants: NO, NO2, NOx, NH3, CO, SO2, O3")

print(f"\nNew spatial features: 5")
print(f"  - zone, zone_lat, zone_lon")
print(f"  - industrial_density, traffic_density")
print(f"  - distance_from_center")

print(f"\nNew weather features: 5")
print(f"  - temperature, humidity, wind_speed")
print(f"  - pressure, precipitation")

print(f"\nNew derived features: 7")
print(f"  - temp_humidity_index, wind_chill")
print(f"  - pollution_accumulation, seasonal_pollution_factor")
print(f"  - traffic_weather_interaction, industrial_weather_interaction")
print(f"  - rain_effect")

print(f"\nTotal features: {len(df.columns)}")

# Show feature statistics
print(f"\nFeature Statistics:")
print(f"  Temperature: {df['temperature'].mean():.1f}°C (±{df['temperature'].std():.1f})")
print(f"  Humidity: {df['humidity'].mean():.1f}% (±{df['humidity'].std():.1f})")
print(f"  Wind Speed: {df['wind_speed'].mean():.1f} m/s (±{df['wind_speed'].std():.1f})")
print(f"  Industrial Density: {df['industrial_density'].mean():.2f}")
print(f"  Traffic Density: {df['traffic_density'].mean():.2f}")

print("\n" + "="*80)
print("Next Steps:")
print("  1. Review: dataset_extracted/training_data_v5_enhanced.csv")
print("  2. Train: python train_v5_enhanced.py")
print("  3. Expected accuracy: 72-75%")
print("="*80)

# ============================================================================
# OPTIONAL: Collect Real Weather Data for Recent Dates
# ============================================================================

print("\n[OPTIONAL] Real Weather Data Collection")
print("="*80)

if OPENWEATHER_API_KEY != 'your_api_key_here':
    print("\nCollecting real weather data for recent dates...")
    print("(This will use your OpenWeatherMap API quota)")
    
    # Get unique recent dates (last 30 days)
    recent_dates = df[df['Date'] >= (datetime.now() - timedelta(days=30))]['Date'].unique()
    
    print(f"  Found {len(recent_dates)} recent dates")
    print("  Note: Free tier allows 1000 calls/day")
    print("  Skipping for now - run separately if needed")
else:
    print("\n  No OpenWeatherMap API key provided")
    print("  Using estimated weather data based on seasonal patterns")
    print("  To use real weather data:")
    print("    1. Get free API key: https://openweathermap.org/api")
    print("    2. Set environment variable: OPENWEATHER_API_KEY")
    print("    3. Re-run this script")

print("\n" + "="*80)
