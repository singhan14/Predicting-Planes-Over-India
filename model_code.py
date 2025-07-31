import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

class FlightPredictor:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.df = None
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_columns = ['hour', 'day_of_week']

    def load_data(self):
        self.df = pd.read_csv(self.csv_file_path)

        # Ensure timestamp column exists and is datetime
        if 'timestamp' not in self.df.columns:
            raise ValueError("CSV must contain a 'timestamp' column")

        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['day_of_week'] = self.df['timestamp'].dt.dayofweek

        # Target column must exist
        if 'count' not in self.df.columns:
            raise ValueError("CSV must contain a 'count' column for target prediction")

    def train_model(self):
        X = self.df[self.feature_columns]
        y = self.df['count']

        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        # Optional evaluation (can be removed in production)
        y_pred = self.model.predict(X_test)
        print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}, R2: {r2_score(y_test, y_pred):.2f}")

    def predict(self, hour, day_of_week):
        X_input = self.scaler.transform([[hour, day_of_week]])
        return self.model.predict(X_input)[0]
