from flask import Flask, request, jsonify
import pandas as pd
from model_code import FlightPredictor  # move your class to model_code.py

app = Flask(__name__)
predictor = FlightPredictor("opensky_india_detailed.csv")
predictor.load_data()
predictor.train_model()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        hour = input_data.get("hour")
        day_of_week = input_data.get("day_of_week")

        prediction = predictor.predict(hour, day_of_week)
        return jsonify({
            "predicted_count": int(prediction),
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500