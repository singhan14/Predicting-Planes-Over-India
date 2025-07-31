# prediction.py

import pandas as pd
import os
from pathlib import Path
import json
from joblib import load

# Load CatBoost model from joblib
model_path = "models/catboost_flight_count_predictor.joblib"
model = load(model_path) if os.path.exists(model_path) else None

# Step 1: Load latest CSV from GitHub raw URL
csv_url = "https://raw.githubusercontent.com/singhan14/Predicting-Planes-Over-India/main/opensky_india_detailed.csv"
df = pd.read_csv(csv_url)

# Step 2: Preprocess timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df.dropna(subset=['timestamp'], inplace=True)

# Step 3: Create time-based features
df['date_only'] = df['timestamp'].dt.date
df['time_only'] = df['timestamp'].dt.strftime('%H:%M')
df['minute_timestamp'] = df['timestamp'].dt.floor('min')

# Step 4: Count flights per minute
minute_flight_counts = df.groupby('minute_timestamp').size().reset_index(name='flight_count_per_minute')
df = pd.merge(df, minute_flight_counts, on='minute_timestamp', how='left')

# Step 5: Aggregate by date_only and time_only
time_features = df.groupby(['date_only', 'time_only'])['flight_count_per_minute'].mean().reset_index()

# Predict using the loaded model
if model:
    # Assuming model expects 'date_only' (as ordinal) and 'time_only' (HH:MM string converted to hour + minute)
    time_features['date_ordinal'] = pd.to_datetime(time_features['date_only']).map(pd.Timestamp.toordinal)
    time_features['hour'] = time_features['time_only'].str.slice(0, 2).astype(int)
    time_features['minute'] = time_features['time_only'].str.slice(3, 5).astype(int)

    X = time_features[['date_ordinal', 'hour', 'minute']]
    time_features['predicted_count'] = model.predict(X)

# Step 6: Save results
Path("predictions").mkdir(exist_ok=True)

# Save as CSV
time_features.to_csv("predictions/flight_count_per_minute.csv", index=False)

# Save as JSON (for dashboard)
json_data = time_features.to_dict(orient="records")
with open("predictions/flight_count_per_minute.json", "w") as f:
    json.dump(json_data, f, indent=2, default=str)

print("✅ Prediction results saved to /predictions/")
