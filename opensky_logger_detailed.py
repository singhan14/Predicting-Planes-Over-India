import requests
import csv
import os
from datetime import datetime, timezone

# Define India bounding box
INDIA_BOUNDS = {
    "min_lat": 6,
    "max_lat": 37,
    "min_lon": 68,
    "max_lon": 97
}

# Define central coordinates of India for distance estimation (optional)
INDIA_CENTER_LAT = 23.5937
INDIA_CENTER_LON = 80.9629

# Output file
CSV_FILE = "opensky_india_detailed.csv"

# CSV Header with added features
CSV_HEADER = [
    "timestamp", "icao24", "callsign", "origin_country",
    "latitude", "longitude", "baro_altitude", "geo_altitude",
    "on_ground", "velocity", "true_track", "vertical_rate",
    "hour", "day_of_week", "is_weekend", "flight_phase",
    "airline_code"
]

# Write header if file doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)

def classify_flight_phase(vertical_rate):
    if vertical_rate is None:
        return "unknown"
    if vertical_rate > 3:
        return "climb"
    elif vertical_rate < -3:
        return "descent"
    else:
        return "cruise"

def log_planes_over_india_detailed():
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    data = response.json()

if not data or "states" not in data or data["states"] is None:
    print("No valid 'states' data returned from OpenSky API.")
    return

    timestamp = datetime.now(timezone.utc)
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    hour = timestamp.hour
    day_of_week = timestamp.weekday()
    is_weekend = day_of_week >= 5

    rows = []
    for plane in data.get("states", []):
        lon = plane[5]
        lat = plane[6]
        if lon and lat and \
           INDIA_BOUNDS["min_lon"] <= lon <= INDIA_BOUNDS["max_lon"] and \
           INDIA_BOUNDS["min_lat"] <= lat <= INDIA_BOUNDS["max_lat"]:

            icao24 = plane[0]
            callsign = plane[1].strip() if plane[1] else ""
            origin_country = plane[2]
            baro_altitude = plane[7]
            geo_altitude = plane[13]
            on_ground = plane[8]
            velocity = plane[9]
            true_track = plane[10]
            vertical_rate = plane[11]

            flight_phase = classify_flight_phase(vertical_rate)
            airline_code = callsign[:2] if callsign else ""

            row = [
                timestamp_str, icao24, callsign, origin_country,
                lat, lon, baro_altitude, geo_altitude,
                on_ground, velocity, true_track, vertical_rate,
                hour, day_of_week, is_weekend, flight_phase,
                airline_code
            ]
            rows.append(row)

    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ Logged {len(rows)} planes at {timestamp_str}")

if __name__ == "__main__":
    log_planes_over_india_detailed()
