import pandas as pd
import numpy as np
from datetime import datetime

class FlightPredictor:
    def __init__(self):
        pass  # You can load trained models here later if needed

    def predict(self, target_datetime, model_type, weather_factor, df):
        # Preprocess
        df['timestamp'] = pd.to_datetime(df['time'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek

        # Aggregate flights
        df_grouped = df.groupby(['hour', 'day_of_week']).size().reset_index(name='flight_count')

        # Parse target date
        target_dt = pd.to_datetime(target_datetime)
        target_hour = target_dt.hour
        target_dayofweek = target_dt.dayofweek

        # Get base flight count from historical average
        relevant_rows = df_grouped[(df_grouped['hour'] == target_hour) & (df_grouped['day_of_week'] == target_dayofweek)]
        base_count = int(relevant_rows['flight_count'].mean()) if not relevant_rows.empty else 20

        # Model adjustment
        model_multiplier = {
            'lstm': 1.0,
            'arima': 0.95,
            'ensemble': 1.05
        }

        # Weather adjustment
        weather_multiplier = {
            'clear': 1.0,
            'cloudy': 0.95,
            'rainy': 0.7,
            'stormy': 0.4
        }

        adjusted_count = int(base_count * model_multiplier.get(model_type, 1.0) * weather_multiplier.get(weather_factor, 1.0))

        confidence = max(60, min(95, 85 - abs(target_hour - 12) * 2))  # simulate confidence

        prediction = {
            "count": adjusted_count,
            "confidence": confidence,
            "hourlyBreakdown": self.generate_hourly_breakdown(df_grouped, target_dayofweek),
            "altitudeDistribution": self.generate_altitude_distribution(adjusted_count),
            "detailedFlights": self.generate_flight_details(adjusted_count, target_dt)
        }

        return prediction

    def generate_hourly_breakdown(self, df_grouped, target_dayofweek):
        hourly = []
        for hour in range(24):
            rows = df_grouped[(df_grouped['hour'] == hour) & (df_grouped['day_of_week'] == target_dayofweek)]
            mean_count = int(rows['flight_count'].mean()) if not rows.empty else 10
            noisy_count = max(5, int(mean_count + np.random.randn() * 3))
            hourly.append(noisy_count)
        return hourly

    def generate_altitude_distribution(self, total_count):
        # Distribute total_count into altitude bands
        dist = np.random.dirichlet(np.ones(5)) * total_count
        return [int(x) for x in dist]

    def generate_flight_details(self, count, target_dt):
        airlines = ['AI', '6E', 'SG', 'UK', 'G8', 'I5', 'QP']
        origins = ['India', 'USA', 'Germany', 'UAE', 'France', 'Singapore']
        flights = []

        for _ in range(min(count, 12)):
            airline = np.random.choice(airlines)
            number = np.random.randint(1000, 9999)
            altitude = np.random.randint(5000, 40000)
            speed = np.random.randint(300, 700)
            conf = np.random.randint(70, 95)
            time_est = (target_dt + pd.Timedelta(minutes=np.random.randint(0, 60))).strftime("%H:%M:%S")

            flights.append({
                "callsign": f"{airline}{number}",
                "origin": np.random.choice(origins),
                "altitude": altitude,
                "speed": speed,
                "confidence": conf,
                "estimatedTime": time_est
            })

        return sorted(flights, key=lambda x: x['estimatedTime'])
