from flask import Flask, request, jsonify
import pandas as pd
from model_code import FlightPredictor  # Make sure this file exists

app = Flask(__name__)

# Load and train the model once at startup
predictor = FlightPredictor("opensky_india_detailed.csv")
predictor.load_data()
predictor.train_model()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "🛫 Flight Predictor API is running", "status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json(force=True)
        hour = input_data.get("hour")
        day_of_week = input_data.get("day_of_week")

        # Validate input
        if hour is None or day_of_week is None:
            return jsonify({"error": "Missing 'hour' or 'day_of_week' in input", "status": "failed"}), 400

        prediction = predictor.predict(hour, day_of_week)
        return jsonify({
            "predicted_count": int(prediction),
            "hour": hour,
            "day_of_week": day_of_week,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
