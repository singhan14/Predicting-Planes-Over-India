from flask import Flask, jsonify
import pandas as pd
import os
import json
from joblib import load

app = Flask(__name__)

model_path = "catboost_flight_count_predictor.joblib"
model = load(model_path)

@app.route("/")
def index():
    return jsonify({"message": "Flight Prediction API is running."})

@app.route("/predict")
def predict():
    csv_url = "https://raw.githubusercontent.com/singhan14/Predicting-Planes-Over-India/main/opensky_india_detailed.csv"
    df = pd.read_csv(csv_url)

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)

    df['date_only'] = df['timestamp'].dt.date
    df['time_only'] = df['timestamp'].dt.strftime('%H:%M')
    df['minute_timestamp'] = df['timestamp'].dt.floor('min')

    minute_flight_counts = df.groupby('minute_timestamp').size().reset_index(name='flight_count_per_minute')
    df = pd.merge(df, minute_flight_counts, on='minute_timestamp', how='left')

    time_features = df.groupby(['date_only', 'time_only'])['flight_count_per_minute'].mean().reset_index()

    time_features['date_ordinal'] = pd.to_datetime(time_features['date_only']).map(pd.Timestamp.toordinal)
    time_features['hour'] = time_features['time_only'].str.slice(0, 2).astype(int)
    time_features['minute'] = time_features['time_only'].str.slice(3, 5).astype(int)

    X = time_features[['date_ordinal', 'hour', 'minute']]
    time_features['predicted_count'] = model.predict(X)

    json_data = time_features.to_dict(orient="records")
    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug=True)
