from flask import Flask, request, jsonify
import pandas as pd
from model_code import FlightPredictor  # assuming this contains your prediction logic
import os

app = Flask(__name__)
MODEL = FlightPredictor()  # initialize your model once

CSV_PATH = os.path.join(os.path.dirname(__file__), "opensky_india_detailed.csv")

@app.route('/')
def health():
    return jsonify({"status": "API is running"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        target_datetime = data.get("target_datetime")
        model_type = data.get("model_type", "ensemble")
        weather_factor = data.get("weather_factor", "clear")

        # Load the latest data
        df = pd.read_csv(CSV_PATH)

        # Call your prediction logic
        result = MODEL.predict(target_datetime, model_type, weather_factor, df)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
