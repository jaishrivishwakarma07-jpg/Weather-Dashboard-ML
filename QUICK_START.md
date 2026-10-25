# 🚀 Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell/Command Prompt in project folder:

```bash
cd weather_dashboard_project
pip install -r requirements.txt
```

Expected output (takes 2-3 minutes):
```
Successfully installed requests scikit-learn pandas numpy python-dotenv
```

## Step 2: Verify Setup

Check if API key is loaded:
```bash
cd src
python -c "from weather_api import WeatherAPI; api = WeatherAPI(); print('✅ API Key loaded!')"
```

## Step 3: Run Dashboard

```bash
python main.py
```

## First Run Checklist

- [ ] Type your city name (e.g., "Mumbai", "London", "New York")
- [ ] Click "Search" button
- [ ] See current weather displayed
- [ ] Check ML Predictions tab
- [ ] View 5-day Forecast

## Features Overview

### 🌡️ Current Weather Tab
- Real-time data from OpenWeatherMap
- Temperature, humidity, wind, pressure
- Smart weather recommendations based on conditions

### 🤖 ML Predictions Tab
- Temperature forecast using Linear Regression
- Rain probability using Random Forest
- Trained on weatherHistory.csv data

### 📅 Forecast Tab
- 5-day weather prediction
- Hourly breakdown
- Rain probabilities

## Common Issues & Solutions

### Issue: "WEATHER_API_KEY not found"
**Solution:** Verify `.env` file exists in project root with:
```
WEATHER_API_KEY=86d78a7561a6ecb134c842432532b234
```

### Issue: "City not found"
**Solution:** Use English city names (e.g., "Tokyo" not "टोक्यो")

### Issue: ML Predictions showing "N/A"
**Solution:** weatherHistory.csv should be in parent directory for better predictions

### Issue: Application is slow
**Solution:** First API call takes 2-3 seconds (normal). Subsequent calls are faster.

## Project Files Explained

```
weather_dashboard_project/
│
├── src/
│   ├── main.py              👈 Run this! (Desktop app)
│   ├── weather_api.py       (API calls to OpenWeatherMap)
│   ├── ml_prediction.py     (Temperature & rain predictions)
│   └── data_handler.py      (CSV data management)
│
├── .env                     (Contains your API key)
├── requirements.txt         (Python packages needed)
├── README.md               (Full documentation)
└── QUICK_START.md          (This file)
```

## Playing with the App

### Change Default City
In `src/main.py`, line find:
```python
self.city_entry.insert(0, "Delhi")
```
Change to your preferred city.

### Train on Historical Data
Place weatherHistory.csv in parent directory:
```
weather_dashboard_project/../weatherHistory.csv
```

Then ML models will be trained automatically.

### Change UI Colors
In `src/main.py` `setup_ui()` function, modify:
```python
bg='#1e1e1e'  # Dark background
fg='#4da6ff'  # Text color
```

## What's Next?

1. **Test with multiple cities** - See predictions for different locations
2. **Check forecast accuracy** - Compare predictions with actual
3. **Enhance ML models** - Add more features for better predictions
4. **Add notifications** - Set alerts for specific weather conditions

## API Documentation

**OpenWeatherMap (Free Tier)**
- 60 requests/minute limit
- Current weather data
- 5-day forecast
- No credit card required

Get API key: https://openweathermap.org

## Python Concepts Used

✅ Object-Oriented Programming (Classes)
✅ API Integration (Requests library)
✅ Machine Learning (Scikit-learn)
✅ GUI Development (Tkinter)
✅ Threading (Async operations)
✅ Environment Variables (.env)
✅ Data Processing (Pandas)

## Performance Tips

- First search may take 2-3 seconds
- Subsequent searches are faster (cached predictions)
- ML models train once at startup
- API calls run in background threads

---

**Enjoy your Weather Dashboard! 🌤️**

For detailed info, read: README.md
