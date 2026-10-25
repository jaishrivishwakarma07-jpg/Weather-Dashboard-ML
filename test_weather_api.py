"""
Unit tests for weather_api.py
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather_api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = 'test_api_key'
        self.city = 'London'

    @patch('weather_api.os.getenv')
    def test_init_success(self, mock_getenv):
        """Test successful initialization"""
        mock_getenv.return_value = self.api_key

        api = WeatherAPI()
        self.assertEqual(api.api_key, self.api_key)
        self.assertEqual(api.base_url, "https://api.openweathermap.org/data/2.5/weather")

    @patch('weather_api.os.getenv')
    def test_init_no_api_key(self, mock_getenv):
        """Test initialization failure when API key is missing"""
        mock_getenv.return_value = None

        with self.assertRaises(ValueError) as context:
            WeatherAPI()

        self.assertIn("WEATHER_API_KEY not found", str(context.exception))

    @patch('weather_api.requests.get')
    @patch('weather_api.os.getenv')
    def test_get_current_weather_success(self, mock_getenv, mock_get):
        """Test successful current weather fetch"""
        mock_getenv.return_value = self.api_key

        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {'temp': 15.5, 'feels_like': 14.0, 'humidity': 65, 'pressure': 1013},
            'weather': [{'main': 'Clouds', 'description': 'scattered clouds'}],
            'wind': {'speed': 3.5},
            'clouds': {'all': 40}
        }
        mock_get.return_value = mock_response

        api = WeatherAPI()
        result = api.get_current_weather(self.city)

        self.assertEqual(result['city'], 'London')
        self.assertEqual(result['country'], 'GB')
        self.assertEqual(result['temperature'], 15.5)
        self.assertEqual(result['weather'], 'Clouds')
        self.assertEqual(result['wind_speed'], 3.5)

    @patch('weather_api.requests.get')
    @patch('weather_api.os.getenv')
    def test_get_current_weather_city_not_found(self, mock_getenv, mock_get):
        """Test current weather fetch for non-existent city"""
        mock_getenv.return_value = self.api_key

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api = WeatherAPI()
        result = api.get_current_weather('NonExistentCity')

        self.assertIn('error', result)
        self.assertIn('404', result['error'])

    @patch('weather_api.requests.get')
    @patch('weather_api.os.getenv')
    def test_get_current_weather_exception(self, mock_getenv, mock_get):
        """Test current weather fetch with network exception"""
        mock_getenv.return_value = self.api_key

        mock_get.side_effect = Exception("Network error")

        api = WeatherAPI()
        result = api.get_current_weather(self.city)

        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Network error')

    @patch('weather_api.requests.get')
    @patch('weather_api.os.getenv')
    def test_get_forecast_success(self, mock_getenv, mock_get):
        """Test successful forecast fetch"""
        mock_getenv.return_value = self.api_key

        # Mock forecast response with more data points
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [
                {
                    'dt_txt': '2024-01-01 12:00:00',
                    'main': {'temp': 16.0, 'humidity': 70},
                    'weather': [{'main': 'Rain'}],
                    'wind': {'speed': 4.0},
                    'pop': 0.8
                },
                {
                    'dt_txt': '2024-01-01 15:00:00',
                    'main': {'temp': 17.0, 'humidity': 65},
                    'weather': [{'main': 'Clouds'}],
                    'wind': {'speed': 3.5},
                    'pop': 0.3
                },
                {
                    'dt_txt': '2024-01-01 18:00:00',
                    'main': {'temp': 15.5, 'humidity': 75},
                    'weather': [{'main': 'Rain'}],
                    'wind': {'speed': 5.0},
                    'pop': 0.9
                },
                {
                    'dt_txt': '2024-01-01 21:00:00',
                    'main': {'temp': 14.0, 'humidity': 80},
                    'weather': [{'main': 'Clouds'}],
                    'wind': {'speed': 4.5},
                    'pop': 0.4
                },
                {
                    'dt_txt': '2024-01-02 00:00:00',
                    'main': {'temp': 13.5, 'humidity': 85},
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 3.0},
                    'pop': 0.1
                },
                {
                    'dt_txt': '2024-01-02 03:00:00',
                    'main': {'temp': 12.0, 'humidity': 90},
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 2.5},
                    'pop': 0.0
                },
                {
                    'dt_txt': '2024-01-02 06:00:00',
                    'main': {'temp': 11.5, 'humidity': 95},
                    'weather': [{'main': 'Clouds'}],
                    'wind': {'speed': 2.0},
                    'pop': 0.2
                },
                {
                    'dt_txt': '2024-01-02 09:00:00',
                    'main': {'temp': 14.0, 'humidity': 70},
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 3.0},
                    'pop': 0.1
                },
                {
                    'dt_txt': '2024-01-02 12:00:00',
                    'main': {'temp': 18.0, 'humidity': 60},
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 2.0},
                    'pop': 0.1
                }
            ]
        }
        mock_get.return_value = mock_response

        api = WeatherAPI()
        result = api.get_forecast(self.city)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['temperature'], 16.0)
        self.assertEqual(result[0]['weather'], 'Rain')
        self.assertEqual(result[0]['rain_probability'], 80.0)
        self.assertEqual(result[1]['temperature'], 18.0)

    @patch('weather_api.requests.get')
    @patch('weather_api.os.getenv')
    def test_get_forecast_api_error(self, mock_getenv, mock_get):
        """Test forecast fetch with API error"""
        mock_getenv.return_value = self.api_key

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        api = WeatherAPI()
        result = api.get_forecast(self.city)

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()