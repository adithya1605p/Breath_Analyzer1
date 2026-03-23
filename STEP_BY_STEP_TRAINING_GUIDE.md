# Step-by-Step Model Training Guide

**Goal:** Improve VayuDrishti accuracy from 69.5% to 85%+

---

## 📚 Part 1: Data Collection

### Step 1: Collect Historical AQI Data (1-2 days)

**What You Need:**
- WAQI API token (you have: `9abbe99f4595fa8a4d20dd26a06db8e375273034`)
- OpenAQ API access (free)
- CPCB data (if available)

**Create Data Collection Script:**

```python
# File: backend/scripts/collect_training_data.py

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

WAQI_TOKEN = os.getenv("WAQI_TOKEN", "9abbe99f4595fa8a4d20dd26a06db8e375273034")

# Delhi monitoring stations
DELHI_STATIONS = [
    {"name": "Mandir Marg", "lat": 28.6341, "lon": 77.2005},
    {"name": "ITO", "lat": 28.6289, "lon": 77.2416},
    {"name": "Anand Vihar", "lat": 28.6469, "lon": 77.3158},
    {"name": "RK Puram", "lat": 28.5629, "lon": 77.1824},
    {"name": "Dwarka", "lat": 28.5921, "lon": 77.0460},
    {"name": "Punjabi Bagh", "lat": 28.6692, "lon": 77.1317},
    {"name": "Rohini", "lat": 28.7041, "lon": 77.1025},
    {"name": "Nehru Nagar", "lat": 28.5706, "lon": 77.2514},
    {"name": "Vivek Vihar", "lat": 28.6692, "lon": 77.3152},
    {"name": "Shadipur", "lat": 28.6517, "lon": 77.1583},
]

def fetch_current_data(station):
    """Fetch current AQI data for a station"""
    try:
        url = f"https://api.waqi.info/feed/geo:{station['lat']};{station['lon']}/"
        response = requests.get(url, params={"token": WAQI_TOKEN}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                result = data.get("data", {})
                iaqi = result.get("iaqi", {})
                
                return {
                    "timestamp": datetime.now(),
                    "station_name": station["name"],
                    "lat": station["lat"],
                    "lon": station["lon"],
                    "aqi": result.get("aqi"),
                    "pm25": iaqi.get("pm25", {}).get("v"),
                    "pm10": iaqi.get("pm10", {}).get("v"),
                    "no2": iaqi.get("no2", {}).get("v"),
                    "so2": iaqi.get("so2", {}).get("v"),
                    "co": iaqi.get("co", {}).get("v"),
                    "o3": iaqi.get("o3", {}).get("v"),
                    "temp": iaqi.get("t", {}).get("v"),
                    "humidity": iaqi.get("h", {}).get("v"),
                    "pressure": iaqi.get("p", {}).get("v"),
                    "wind_speed": iaqi.get("w", {}).get("v"),
                    "wind_direction": iaqi.get("wd", {}).get("v"),
                }
    except Exception as e:
        print(f"Error fetching {station['name']}: {e}")
    return None

def collect_realtime_data(hours=24):
    """Collect data every hour for specified hours"""
    all_data = []
    
    for hour in range(hours):
        print(f"\n[Hour {hour+1}/{hours}] Collecting data...")
        
        for station in DELHI_STATIONS:
            data = fetch_current_data(station)
            if data:
                all_data.append(data)
                print(f"  ✓ {station['name']}: AQI {data['aqi']}")
            time.sleep(2)  # Rate limiting
        
        if hour < hours - 1:
            print(f"Waiting 1 hour...")
            time.sleep(3600)  # Wait 1 hour
    
    # Save to CSV
    df = pd.DataFrame(all_data)
    filename = f"delhi_aqi_realtime_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved {len(df)} records to {filename}")
    return df

if __name__ == "__main__":
    # Collect 24 hours of data
    df = collect_realtime_data(hours=24)
```

**Run the script:**
```bash
cd backend/scripts
python collect_training_data.py
```

**Expected Output:**
- CSV file with hourly data from 10 stations
- ~240 data points (10 stations × 24 hours)

---

### Step 2: Download Historical Data (1 day)

**Option A: Use Existing Datasets**

You already have:
- `backend/dataset_extracted/city_day.csv` - Historical Indian city data
- `backend/delhi_historical_aqi.csv` - Delhi historical data

**Load and inspect:**
```python
import pandas as pd

# Load existing data
city_data = pd.read_csv('backend/dataset_extracted/city_day.csv')
delhi_data = pd.read_csv('backend/delhi_historical_aqi.csv')

print("City Data Shape:", city_data.shape)
print("Delhi Data Shape:", delhi_data.shape)
print("\nCity Data Columns:", city_data.columns.tolist())
print("\nDelhi Data Sample:")
print(delhi_data.head())
```

**Option B: Download from OpenAQ**

```python
# File: backend/scripts/download_openaq_data.py

import requests
import pandas as pd
from datetime import datetime, timedelta

def download_openaq_delhi(days=365):
    """Download historical data from OpenAQ"""
    
    # Delhi bounding box
    bbox = "28.4,76.8,28.9,77.4"
    
    all_data = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        
        url = "https://api.openaq.org/v2/measurements"
        params = {
            "date_from": date,
            "date_to": date,
            "limit": 1000,
            "page": 1,
            "offset": 0,
            "sort": "desc",
            "radius": 50000,
            "coordinates": "28.6139,77.2090",  # Delhi center
            "order_by": "datetime",
            "parameter": ["pm25", "pm10", "no2", "so2", "co", "o3"]
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                for r in results:
                    all_data.append({
                        "date": r.get("date", {}).get("utc"),
                        "location": r.get("location"),
                        "city": r.get("city"),
                        "parameter": r.get("parameter"),
                        "value": r.get("value"),
                        "unit": r.get("unit"),
                        "lat": r.get("coordinates", {}).get("latitude"),
                        "lon": r.get("coordinates", {}).get("longitude"),
                    })
                
                print(f"✓ Downloaded {len(results)} records for {date}")
        except Exception as e:
            print(f"✗ Error for {date}: {e}")
    
    df = pd.DataFrame(all_data)
    df.to_csv(f"openaq_delhi_{days}days.csv", index=False)
    return df

if __name__ == "__main__":
    df = download_openaq_delhi(days=365)  # 1 year
```

---

### Step 3: Data Preprocessing (1 day)

**Create preprocessing script:**

```python
# File: backend/scripts/preprocess_training_data.py

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_merge_data():
    """Load all available datasets and merge"""
    
    # Load datasets
    city_data = pd.read_csv('backend/dataset_extracted/city_day.csv')
    delhi_hist = pd.read_csv('backend/delhi_historical_aqi.csv')
    
    # Filter for Delhi only
    delhi_city = city_data[city_data['City'] == 'Delhi'].copy()
    
    # Standardize column names
    delhi_city.columns = delhi_city.columns.str.lower()
    delhi_hist.columns = delhi_hist.columns.str.lower()
    
    # Merge datasets
    combined = pd.concat([delhi_city, delhi_hist], ignore_index=True)
    
    # Remove duplicates
    combined = combined.drop_duplicates(subset=['date'], keep='last')
    
    return combined

def add_temporal_features(df):
    """Add time-based features"""
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Season
    df['season'] = df['month'].map({
        12: 'winter', 1: 'winter', 2: 'winter',
        3: 'spring', 4: 'spring', 5: 'spring',
        6: 'summer', 7: 'summer', 8: 'summer',
        9: 'autumn', 10: 'autumn', 11: 'autumn'
    })
    
    return df

def add_spatial_features(df, ward_geojson_path):
    """Add spatial features based on ward locations"""
    import json
    
    # Load ward GeoJSON
    with open(ward_geojson_path, 'r') as f:
        wards = json.load(f)
    
    # For each data point, find nearest ward
    # Add ward-specific features
    
    # Distance from city center
    delhi_center = (28.6139, 77.2090)
    df['dist_from_center'] = np.sqrt(
        (df['lat'] - delhi_center[0])**2 + 
        (df['lon'] - delhi_center[1])**2
    )
    
    return df

def handle_missing_values(df):
    """Handle missing values intelligently"""
    
    # For pollutants, use forward fill then backward fill
    pollutant_cols = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
    
    for col in pollutant_cols:
        if col in df.columns:
            # Forward fill (use previous value)
            df[col] = df[col].fillna(method='ffill', limit=3)
            # Backward fill for remaining
            df[col] = df[col].fillna(method='bfill', limit=3)
            # Fill remaining with median
            df[col] = df[col].fillna(df[col].median())
    
    return df

def create_training_dataset():
    """Main preprocessing pipeline"""
    
    print("Step 1: Loading data...")
    df = load_and_merge_data()
    print(f"  Loaded {len(df)} records")
    
    print("\nStep 2: Adding temporal features...")
    df = add_temporal_features(df)
    
    print("\nStep 3: Handling missing values...")
    df = handle_missing_values(df)
    
    print("\nStep 4: Removing outliers...")
    # Remove extreme outliers (likely sensor errors)
    for col in ['pm25', 'pm10']:
        if col in df.columns:
            q1 = df[col].quantile(0.01)
            q99 = df[col].quantile(0.99)
            df = df[(df[col] >= q1) & (df[col] <= q99)]
    
    print(f"\nFinal dataset: {len(df)} records")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nColumns: {df.columns.tolist()}")
    
    # Save
    df.to_csv('training_data_processed.csv', index=False)
    print("\n✓ Saved to training_data_processed.csv")
    
    return df

if __name__ == "__main__":
    df = create_training_dataset()
```

**Run preprocessing:**
```bash
python backend/scripts/preprocess_training_data.py
```

---

## 🧠 Part 2: Model Training

### Step 4: Design Improved Model Architecture (1 day)

**Current Model Issues:**
1. Only predicts PM2.5
2. Doesn't capture PM10 spikes
3. No temporal patterns
4. Limited spatial features

**New Model Design:**

```python
# File: backend/app/ml/improved_model.py

import torch
import torch.nn as nn

class ImprovedAQIPredictor(nn.Module):
    """
    Multi-output model predicting both PM2.5 and PM10
    with attention mechanism for temporal patterns
    """
    
    def __init__(self, 
                 input_dim=20,  # More features
                 hidden_dim=256,
                 num_layers=3,
                 dropout=0.3):
        super().__init__()
        
        # Feature embedding
        self.feature_embed = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Spatial attention
        self.spatial_attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Softmax(dim=1)
        )
        
        # Deep layers
        layers = []
        for i in range(num_layers):
            layers.extend([
                nn.Linear(hidden_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
        self.deep_layers = nn.Sequential(*layers)
        
        # Output heads
        self.pm25_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        self.pm10_head = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
    def forward(self, x):
        # Embed features
        x = self.feature_embed(x)
        
        # Apply spatial attention
        attention_weights = self.spatial_attention(x)
        x = x * attention_weights
        
        # Deep processing
        x = self.deep_layers(x)
        
        # Predict both PM2.5 and PM10
        pm25 = self.pm25_head(x)
        pm10 = self.pm10_head(x)
        
        return pm25, pm10
```

---

### Step 5: Feature Engineering (1 day)

**Create comprehensive feature set:**

```python
# File: backend/scripts/create_features.py

import pandas as pd
import numpy as np

def create_features(df):
    """Create all features for training"""
    
    features = pd.DataFrame()
    
    # 1. Basic spatial features
    features['lat'] = df['lat']
    features['lon'] = df['lon']
    features['dist_from_center'] = df['dist_from_center']
    
    # 2. Temporal features
    features['month'] = df['month']
    features['day_of_week'] = df['day_of_week']
    features['day_of_year'] = df['day_of_year']
    features['is_weekend'] = df['is_weekend']
    
    # Season encoding (one-hot)
    season_dummies = pd.get_dummies(df['season'], prefix='season')
    features = pd.concat([features, season_dummies], axis=1)
    
    # 3. Meteorological features
    if 'temp' in df.columns:
        features['temp'] = df['temp']
    if 'humidity' in df.columns:
        features['humidity'] = df['humidity']
    if 'wind_speed' in df.columns:
        features['wind_speed'] = df['wind_speed']
    if 'pressure' in df.columns:
        features['pressure'] = df['pressure']
    
    # 4. Other pollutants (correlated with PM)
    if 'no2' in df.columns:
        features['no2'] = df['no2']
    if 'so2' in df.columns:
        features['so2'] = df['so2']
    if 'co' in df.columns:
        features['co'] = df['co']
    if 'o3' in df.columns:
        features['o3'] = df['o3']
    
    # 5. Lagged features (previous day pollution)
    if 'pm25' in df.columns:
        features['pm25_lag1'] = df['pm25'].shift(1)
        features['pm25_lag7'] = df['pm25'].shift(7)  # Week ago
    
    # 6. Rolling statistics
    if 'pm25' in df.columns:
        features['pm25_rolling_mean_7d'] = df['pm25'].rolling(7).mean()
        features['pm25_rolling_std_7d'] = df['pm25'].rolling(7).std()
    
    # Fill NaN from rolling/lagging
    features = features.fillna(method='bfill').fillna(0)
    
    return features

# Targets
def create_targets(df):
    """Create target variables"""
    targets = pd.DataFrame()
    targets['pm25'] = df['pm25']
    targets['pm10'] = df['pm10']
    return targets
```

---

**Continue in next message...**


### Step 6: Train the Model (2-3 days)

**Training script:**

```python
# File: backend/scripts/train_improved_model.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

class AQIDataset(Dataset):
    def __init__(self, features, targets):
        self.features = torch.FloatTensor(features)
        self.targets = torch.FloatTensor(targets)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]

def train_model(epochs=100, batch_size=64, learning_rate=0.001):
    """Main training loop"""
    
    # Load data
    print("Loading data...")
    df = pd.read_csv('training_data_processed.csv')
    
    # Create features and targets
    from create_features import create_features, create_targets
    X = create_features(df)
    y = create_targets(df)
    
    # Remove rows with NaN
    mask = ~(X.isna().any(axis=1) | y.isna().any(axis=1))
    X = X[mask]
    y = y[mask]
    
    print(f"Dataset size: {len(X)} samples")
    print(f"Features: {X.shape[1]}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    with open('improved_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Create datasets
    train_dataset = AQIDataset(X_train_scaled, y_train.values)
    test_dataset = AQIDataset(X_test_scaled, y_test.values)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    
    # Initialize model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    from improved_model import ImprovedAQIPredictor
    model = ImprovedAQIPredictor(input_dim=X.shape[1]).to(device)
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )
    
    # Training loop
    best_loss = float('inf')
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        for features, targets in train_loader:
            features, targets = features.to(device), targets.to(device)
            
            optimizer.zero_grad()
            pm25_pred, pm10_pred = model(features)
            
            # Combined loss
            loss_pm25 = criterion(pm25_pred.squeeze(), targets[:, 0])
            loss_pm10 = criterion(pm10_pred.squeeze(), targets[:, 1])
            loss = loss_pm25 + loss_pm10
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validate
        model.eval()
        test_loss = 0
        with torch.no_grad():
            for features, targets in test_loader:
                features, targets = features.to(device), targets.to(device)
                pm25_pred, pm10_pred = model(features)
                
                loss_pm25 = criterion(pm25_pred.squeeze(), targets[:, 0])
                loss_pm10 = criterion(pm10_pred.squeeze(), targets[:, 1])
                loss = loss_pm25 + loss_pm10
                
                test_loss += loss.item()
        
        train_loss /= len(train_loader)
        test_loss /= len(test_loader)
        
        scheduler.step(test_loss)
        
        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}")
        
        # Save best model
        if test_loss < best_loss:
            best_loss = test_loss
            torch.save(model.state_dict(), 'improved_model_best.pt')
            print(f"  ✓ Saved best model (loss: {best_loss:.4f})")
    
    print("\n✓ Training complete!")
    return model

if __name__ == "__main__":
    model = train_model(epochs=100)
```

**Run training:**
```bash
cd backend/scripts
python train_improved_model.py
```

**Expected output:**
- Training progress for 100 epochs
- Best model saved as `improved_model_best.pt`
- Scaler saved as `improved_scaler.pkl`

---

### Step 7: Evaluate Model (1 day)

**Evaluation script:**

```python
# File: backend/scripts/evaluate_model.py

import torch
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def evaluate_model():
    """Evaluate trained model"""
    
    # Load test data
    df = pd.read_csv('training_data_processed.csv')
    
    from create_features import create_features, create_targets
    X = create_features(df)
    y = create_targets(df)
    
    # Load scaler and model
    import pickle
    with open('improved_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    from improved_model import ImprovedAQIPredictor
    model = ImprovedAQIPredictor(input_dim=X.shape[1])
    model.load_state_dict(torch.load('improved_model_best.pt'))
    model.eval()
    
    # Scale features
    X_scaled = scaler.transform(X)
    X_tensor = torch.FloatTensor(X_scaled)
    
    # Predict
    with torch.no_grad():
        pm25_pred, pm10_pred = model(X_tensor)
    
    pm25_pred = pm25_pred.squeeze().numpy()
    pm10_pred = pm10_pred.squeeze().numpy()
    
    # Calculate metrics
    print("PM2.5 Metrics:")
    print(f"  MAE: {mean_absolute_error(y['pm25'], pm25_pred):.2f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y['pm25'], pm25_pred)):.2f}")
    print(f"  R²: {r2_score(y['pm25'], pm25_pred):.4f}")
    
    print("\nPM10 Metrics:")
    print(f"  MAE: {mean_absolute_error(y['pm10'], pm10_pred):.2f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(y['pm10'], pm10_pred)):.2f}")
    print(f"  R²: {r2_score(y['pm10'], pm10_pred):.4f}")
    
    # Plot predictions vs actual
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    axes[0].scatter(y['pm25'], pm25_pred, alpha=0.5)
    axes[0].plot([0, y['pm25'].max()], [0, y['pm25'].max()], 'r--')
    axes[0].set_xlabel('Actual PM2.5')
    axes[0].set_ylabel('Predicted PM2.5')
    axes[0].set_title('PM2.5 Predictions')
    
    axes[1].scatter(y['pm10'], pm10_pred, alpha=0.5)
    axes[1].plot([0, y['pm10'].max()], [0, y['pm10'].max()], 'r--')
    axes[1].set_xlabel('Actual PM10')
    axes[1].set_ylabel('Predicted PM10')
    axes[1].set_title('PM10 Predictions')
    
    plt.tight_layout()
    plt.savefig('model_evaluation.png')
    print("\n✓ Saved evaluation plot to model_evaluation.png")

if __name__ == "__main__":
    evaluate_model()
```

---

## 📦 Part 3: Deployment

### Step 8: Integrate New Model (1 day)

**Update ML engine:**

```python
# File: backend/app/services/ml_engine_v2.py

import torch
import pickle
import os
import numpy as np

class ImprovedMLEngine:
    """Updated ML engine with PM10 support"""
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        model_path = os.path.join(os.path.dirname(__file__), 'improved_model_best.pt')
        scaler_path = os.path.join(os.path.dirname(__file__), 'improved_scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            from app.ml.improved_model import ImprovedAQIPredictor
            
            # Load scaler
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Load model
            input_dim = self.scaler.n_features_in_
            self.model = ImprovedAQIPredictor(input_dim=input_dim)
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✓ Loaded improved model on {self.device}")
        else:
            print("⚠ Improved model not found, using fallback")
    
    def predict(self, features_dict):
        """
        Predict PM2.5 and PM10 for given features
        
        Args:
            features_dict: Dictionary with keys matching training features
        
        Returns:
            dict: {'pm25': float, 'pm10': float, 'aqi': int}
        """
        if self.model is None or self.scaler is None:
            return self._fallback_prediction(features_dict)
        
        # Prepare features
        features = self._prepare_features(features_dict)
        features_scaled = self.scaler.transform([features])
        features_tensor = torch.FloatTensor(features_scaled).to(self.device)
        
        # Predict
        with torch.no_grad():
            pm25_pred, pm10_pred = self.model(features_tensor)
        
        pm25 = float(pm25_pred.item())
        pm10 = float(pm10_pred.item())
        
        # Calculate AQI (use max of PM2.5 and PM10 AQI)
        aqi_pm25 = self._pm25_to_aqi(pm25)
        aqi_pm10 = self._pm10_to_aqi(pm10)
        aqi = max(aqi_pm25, aqi_pm10)
        
        return {
            'pm25': round(pm25, 1),
            'pm10': round(pm10, 1),
            'aqi': int(aqi),
            'dominant_pollutant': 'PM10' if aqi_pm10 > aqi_pm25 else 'PM2.5'
        }
    
    def _prepare_features(self, features_dict):
        """Convert feature dict to array matching training format"""
        # Extract features in correct order
        # This must match the order used during training
        features = []
        
        # Add all features used during training
        # (This is a simplified example - adjust based on your actual features)
        features.append(features_dict.get('lat', 28.6))
        features.append(features_dict.get('lon', 77.2))
        features.append(features_dict.get('dist_from_center', 0))
        # ... add all other features
        
        return np.array(features)
    
    def _pm25_to_aqi(self, pm25):
        """Convert PM2.5 to AQI (US EPA standard)"""
        breakpoints = [
            (0.0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 350.4, 301, 400),
            (350.5, 500.4, 401, 500),
        ]
        
        for c_lo, c_hi, i_lo, i_hi in breakpoints:
            if c_lo <= pm25 <= c_hi:
                return round(i_lo + (pm25 - c_lo) * (i_hi - i_lo) / (c_hi - c_lo))
        return 500 if pm25 > 500 else 0
    
    def _pm10_to_aqi(self, pm10):
        """Convert PM10 to AQI (US EPA standard)"""
        breakpoints = [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 504, 301, 400),
            (505, 604, 401, 500),
        ]
        
        for c_lo, c_hi, i_lo, i_hi in breakpoints:
            if c_lo <= pm10 <= c_hi:
                return round(i_lo + (pm10 - c_lo) * (i_hi - i_lo) / (c_hi - c_lo))
        return 500 if pm10 > 604 else 0
```

---

### Step 9: Test New Model (1 day)

**Run validation again:**

```bash
cd backend
python test_aqi_validation.py
```

**Expected improvements:**
- Average accuracy: 69.5% → 80%+
- Dwarka accuracy: 38.7% → 70%+
- PM10 detection: ✅ Working

---

## 📊 Summary

**Total Time:** ~2 weeks

**Steps:**
1. ✅ Collect data (2 days)
2. ✅ Preprocess data (1 day)
3. ✅ Design model (1 day)
4. ✅ Engineer features (1 day)
5. ✅ Train model (2-3 days)
6. ✅ Evaluate model (1 day)
7. ✅ Integrate model (1 day)
8. ✅ Test and validate (1 day)

**Expected Results:**
- PM2.5 accuracy: 85%+
- PM10 accuracy: 80%+
- Dwarka fixed: ✅
- Overall AQI accuracy: 80-85%

---

**Next:** See `DWARKA_INVESTIGATION.md` for detailed Dwarka analysis
