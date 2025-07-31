# ✈️ Predicting Planes Over India - Hourly

A real-time aircraft tracking and prediction system that monitors air traffic over India using the OpenSky Network API. This project automatically collects, analyzes, and predicts flight patterns with hourly data updates.

## 🌟 Features

- **Real-time Data Collection**: Fetches live aircraft data from OpenSky Network API
- **Geographic Filtering**: Focuses specifically on flights over Indian airspace
- **Automated Scheduling**: Runs hourly data collection via GitHub Actions
- **Historical Analysis**: Builds a comprehensive dataset for trend analysis
- **Prediction Models**: Implements machine learning models to forecast flight patterns
- **Data Visualization**: Generate insights about air traffic patterns over India

## 🚀 How It Works

1. **Data Collection**: The system automatically queries the OpenSky Network API every hour
2. **Filtering**: Filters aircraft data to focus on Indian airspace boundaries
3. **Storage**: Saves detailed flight information to CSV files with timestamps
4. **Analysis**: Processes historical data to identify patterns and trends
5. **Prediction**: Uses machine learning algorithms to forecast future air traffic

## 📊 Data Structure

The system collects comprehensive flight data including:
- **Aircraft Identification**: ICAO24, callsign, origin country
- **Position Data**: Latitude, longitude, altitude, velocity
- **Flight Details**: Heading, vertical rate, sensors
- **Timestamps**: Data collection time in UTC
- **Geographic Info**: Filtered for Indian airspace coordinates

## 🛠️ Technology Stack

- **Python**: Core programming language
- **OpenSky Network API**: Real-time aircraft data source
- **GitHub Actions**: Automated data collection and deployment
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning models

## 📂 Project Structure

```
predicting-planes-over-india-hourly/
├── .github/
│   └── workflows/
│       └── opensky-logger.yml      # Automated data collection workflow
├── data/
│   └── opensky_india_detailed.csv  # Historical flight data
├── src/
│   ├── opensky_logger_detailed.py  # Main data collection script
│   ├── data_analysis.py            # Data analysis and visualization
│   └── prediction_models.py        # Machine learning models
├── notebooks/
│   ├── exploratory_analysis.ipynb  # Data exploration
│   └── model_development.ipynb     # Model training and testing
├── requirements.txt                # Python dependencies
└── README.md                      # Project documentation
```

## 🔧 Setup and Installation

### Prerequisites
- Python 3.8+
- Git
- GitHub account (for automated workflows)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/singhan14/Predicting-Planes-Over-India-hourly.git
   cd Predicting-Planes-Over-India-hourly
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run data collection manually**
   ```bash
   python src/opensky_logger_detailed.py
   ```

### Automated Data Collection

The project uses GitHub Actions to automatically collect data every hour:
- Workflow runs at the start of each hour (UTC)
- Data is automatically committed to the repository
- No manual intervention required

## 📈 Usage

### Manual Data Collection
```python
from src.opensky_logger_detailed import collect_india_flights
data = collect_india_flights()
print(f"Collected {len(data)} flights over India")
```

### Data Analysis
```python
import pandas as pd
from src.data_analysis import analyze_flight_patterns

# Load historical data
df = pd.read_csv('data/opensky_india_detailed.csv')

# Analyze patterns
patterns = analyze_flight_patterns(df)
```

### Running Predictions
```python
from src.prediction_models import predict_traffic_volume

# Predict next hour's traffic
prediction = predict_traffic_volume(historical_data)
print(f"Predicted flights next hour: {prediction}")
```

## 📊 Data Insights

This project helps answer questions like:
- What are the peak flight hours over India?
- Which routes are most commonly used?
- How does air traffic vary by day of week/season?
- Can we predict traffic congestion in Indian airspace?

## 🔄 Automated Workflow

The GitHub Actions workflow:
- **Trigger**: Runs every hour at minute 0
- **Process**: Fetches current aircraft data over India
- **Storage**: Appends data to CSV file
- **Commit**: Automatically commits updated data to repository

## 🌍 Geographic Coverage

**Indian Airspace Boundaries:**
- North: 37°N (Kashmir)
- South: 6°N (Southern tip)
- East: 97°E (Arunachal Pradesh)  
- West: 68°E (Gujarat border)

## 📋 Requirements

Create a `requirements.txt` file with:
```
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
python-dateutil>=2.8.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis feature'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## 📝 API Usage Notes

- Uses OpenSky Network REST API (free tier)
- Rate limited to 4000 API credits per day
- Data collection focuses on Indian airspace coordinates
- Respects API terms of service for non-commercial research

## 🎯 Future Enhancements

- [ ] Real-time web dashboard
- [ ] Weather data integration
- [ ] Flight delay predictions
- [ ] Airport traffic analysis
- [ ] Mobile app development
- [ ] Advanced ML models (LSTM, Prophet)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenSky Network](https://opensky-network.org/) for providing free aircraft data
- GitHub Actions for automated workflow capabilities
- Python community for excellent data science libraries

## 📞 Contact

- **Author**: [Singhan Yadav]
- **GitHub**: [@singhan14](https://github.com/singhan14)
- **Email**: [singhanyadav12@gmail.com]

---

⭐ **Star this repository if you find it useful!**

*Last updated: July 2025*
