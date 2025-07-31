# retrain_model.py

import pandas as pd
import joblib
from model_code import FlightPredictor

# Load the raw OpenSky data
df = pd.read_csv("opensky_india_detailed.csv")

# Extract date & hour for grouping
df['time'] = pd.to_datetime(df['time'])
df['day_of_week'] = df['time'].dt.dayofweek
df['hour'] = df['time'].dt.hour

# Group by hour & weekday to count flights
grouped = df.groupby(['day_of_week', 'hour']).size().reset_index(name='flight_count')
grouped.to_csv('training_data.csv', index=False)

# Train the model
X = grouped[['day_of_week', 'hour']]
y = grouped['flight_count']
model = FlightPredictor()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'model.pkl')
print("✅ Model retrained and saved as model.pkl")
