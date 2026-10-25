# 🌤️ Weather Dashboard with ML Predictions

A desktop weather application built with Python, Tkinter, Machine Learning predictions, and OpenWeatherMap API.

## Features

✨ **Current Weather Display**
- Real-time temperature, humidity, wind speed, and pressure
- Weather conditions with detailed description
- Smart weather recommendations

🤖 **Machine Learning Predictions**
- Temperature prediction based on atmospheric conditions
- Rain probability forecast
- Pattern analysis from historical data
- Weather trend analysis

📅 **5-Day Forecast**
- Detailed forecast for upcoming days
- Temperature trends
- Rain probability

🌍 **Multi-Location Support**
- Search weather for any city worldwide
- Support for cities with same names in different countries

## Project Structure

```
weather_dashboard_project/
├── src/
│   ├── main.py              # Desktop GUI application
│   ├── weather_api.py       # OpenWeatherMap API integration
│   └── ml_prediction.py     # ML models for predictions
├── models/                  # Saved ML models (cache)
├── data/                    # Historical data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenWeatherMap API key (free tier available)

## Installation

1. **Clone/Setup the project**
   ```bash
   cd weather_dashboard_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup .env file**
   Create a `.env` file in the parent directory:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

4. **Get API Key**
   - Visit: https://openweathermap.org/api
   - Sign up for free account
   - Generate API key from dashboard

## Usage

### Run Desktop Application
```bash
cd src
python main.py
```

### Application Interface

**Tab 1: Current Weather**
- Display current weather conditions
- Location name and country
- Temperature, humidity, wind speed
- Smart recommendations

**Tab 2: ML Predictions**
- Temperature prediction
- Rain probability
- AI-based analysis

**Tab 3: Forecast**
- 5-day weather forecast
- Hourly trends
- Predictions

## How ML Works

### Training Data
- Uses `weatherHistory.csv` with historical data
- Extracts patterns from temperature, humidity, pressure, wind

### Algorithms
- **Temperature Prediction**: Linear Regression
  - Learns relationship between atmospheric conditions and temperature
  
- **Rain Prediction**: Random Forest Classifier
  - Classifies if it will rain based on conditions
  - Provides probability scores

### Features Used
- Humidity
- Atmospheric Pressure
- Wind Speed
- Cloud Coverage

## API Integration

Uses **OpenWeatherMap API**:
- Current weather endpoint
- 5-day forecast endpoint
- Metric units (Celsius, m/s)

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Tkinter** | Desktop GUI |
| **Requests** | API calls |
| **Scikit-learn** | ML models |
| **Pandas** | Data handling |
| **NumPy** | Numerical calculations |
| **Python-dotenv** | Environment variables |

## Configuration

Edit in `src/weather_api.py`:
```python
self.base_url = "https://api.openweathermap.org/data/2.5/weather"
self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
```

## Customization

### Change Default City
In `src/main.py`:
```python
self.city_entry.insert(0, "Your_City_Name")
```

### Toggle ML Predictions
In `src/ml_prediction.py`, comment out functions to disable features.

### Change UI Theme
Colors defined in `setup_ui()` with format `#RRGGBB`:
- `#1e1e1e` = Dark background
- `#4da6ff` = Blue accent
- `#ffcc00` = Yellow text

## Troubleshooting

**API Key Error**
- Verify `.env` file exists
- Check API key is correct
- Ensure API key is active on OpenWeatherMap

**City Not Found**
- Use English city name
- Check spelling
- Try full name with country code

**ML Model Issues**
- Ensure `weatherHistory.csv` exists in parent directory
- Check CSV has required columns
- Minimum 10 records needed for training

## Future Enhancements

- [ ] Add multiple city comparison
- [ ] Weather alerts and notifications
- [ ] Historical data visualization
- [ ] Export reports to PDF
- [ ] Location-based recommendations
- [ ] Air quality index integration
- [ ] Dark/Light theme toggle

## License

Free to use and modify

## Support

For issues or suggestions, check:
- OpenWeatherMap API documentation
- Scikit-learn documentation
- Tkinter guide

---

Made with ❤️ for weather enthusiasts
