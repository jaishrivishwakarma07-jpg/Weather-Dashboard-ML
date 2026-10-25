"""
Weather API Integration Module
Fetch weather data from OpenWeatherMap API
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        
        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not found in .env file")
    
    def get_current_weather(self, city):
        """
        Get current weather for a city
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'cloudiness': data['clouds']['all'],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'error': f"City not found or API error: {response.status_code}"}
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_forecast(self, city):
        """
        Get 5-day forecast for a city
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.forecast_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                for item in data['list'][::8]:  # Every 24 hours
                    forecasts.append({
                        'timestamp': item['dt_txt'],
                        'temperature': item['main']['temp'],
                        'weather': item['weather'][0]['main'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed'],
                        'rain_probability': item.get('pop', 0) * 100
                    })
                
                return forecasts
            else:
                return []
                
        except Exception as e:
            print(f"Error: {e}")
            return []
