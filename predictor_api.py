from flask import Flask, request, jsonify
import pandas as pd
import os
from joblib import load
from datetime import datetime

app = Flask(__name__)

# Load trained model
model_path = "catboost_flight_count_predictor.joblib"
model = load(model_path) if os.path.exists(model_path) else None

@app.route("/")
def home():
    return jsonify({"message": "Flight Predictor API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"error": "Model not found"}), 500

    try:
        data = request.json
        date_str = data.get("date")  # Format: YYYY-MM-DD
        time_str = data.get("time")  # Format: HH:MM

        # Parse inputs
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        hour = int(time_str.split(":")[0])
        minute = int(time_str.split(":")[1])

        # Create input DataFrame
        date_ordinal = pd.Timestamp(date_obj).toordinal()
        input_df = pd.DataFrame([[date_ordinal, hour, minute]],
                                columns=["date_ordinal", "hour", "minute"])

        # Predict
        prediction = model.predict(input_df)[0]

        return jsonify({
            "date": date_str,
            "time": time_str,
            "predicted_flight_count": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
