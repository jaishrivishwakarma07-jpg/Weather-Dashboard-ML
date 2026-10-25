"""
Integration tests for the weather dashboard system
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weather_api import WeatherAPI
from data_handler import DataHandler
from ml_prediction import WeatherPredictor

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Set up integration test environment"""
        self.api_key = 'test_api_key'

        # Mock environment variable
        with patch('weather_api.os.getenv', return_value=self.api_key):
            self.api = WeatherAPI()

        self.handler = DataHandler()
        self.predictor = WeatherPredictor()

    @patch('weather_api.requests.get')
    def test_full_weather_workflow(self, mock_get):
        """Test the complete workflow: fetch -> save -> analyze -> predict"""
        # Mock API response
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

        # Step 1: Fetch current weather
        weather_data = self.api.get_current_weather('London')
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['city'], 'London')
        self.assertEqual(weather_data['temperature'], 15.5)

        # Step 2: Save weather record (using temp file)
        import tempfile
        temp_dir = tempfile.mkdtemp()
        original_path = self.handler.csv_path
        test_csv = os.path.join(temp_dir, 'test_weather.csv')
        self.handler.csv_path = test_csv

        try:
            self.handler.save_weather_record('London', weather_data)

            # Verify data was saved
            df = pd.read_csv(test_csv)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]['City'], 'London')
            self.assertEqual(df.iloc[0]['Temperature'], 15.5)

            # Step 3: Train ML model with the saved data
            # Add more data for training
            additional_data = pd.DataFrame({
                'City': ['London'] * 15,
                'Temperature': [15 + i*0.5 for i in range(15)],
                'Humidity': [60 + i for i in range(15)],
                'Pressure': [1010 + i for i in range(15)],
                'Wind Speed': [3 + i*0.2 for i in range(15)],
                'Cloudiness': [30 + i*2 for i in range(15)],
                'Weather': ['Clear' if i % 3 == 0 else 'Clouds' if i % 3 == 1 else 'Rain' for i in range(15)]
            })
            full_data = pd.concat([df, additional_data], ignore_index=True)
            full_data.to_csv(test_csv, index=False)

            # Train the model
            success = self.predictor.train_from_history(test_csv)
            self.assertTrue(success)
            self.assertTrue(self.predictor.is_trained)

            # Step 4: Make predictions
            temp_pred = self.predictor.predict_temperature(65, 1013, 3.5, 40)
            self.assertIsNotNone(temp_pred)

            rain_pred, rain_prob = self.predictor.predict_rain(65, 1013, 3.5, 40)
            self.assertIsNotNone(rain_pred)
            self.assertIsNotNone(rain_prob)

            # Step 5: Generate weather summary
            summary = self.predictor.get_weather_summary(weather_data)
            self.assertIsInstance(summary, str)
            self.assertGreater(len(summary), 0)

        finally:
            self.handler.csv_path = original_path
            if os.path.exists(test_csv):
                os.remove(test_csv)
            os.rmdir(temp_dir)

    def test_data_analysis_workflow(self):
        """Test data analysis workflow: load -> stats -> insights"""
        import tempfile
        temp_dir = tempfile.mkdtemp()
        test_csv = os.path.join(temp_dir, 'analysis_weather.csv')

        # Create comprehensive test data
        test_data = pd.DataFrame({
            'City': ['London'] * 20 + ['Paris'] * 15,
            'Temperature': [15 + i*0.3 for i in range(20)] + [18 + i*0.4 for i in range(15)],
            'Humidity': [60 + i for i in range(20)] + [55 + i for i in range(15)],
            'Pressure': [1010 + i for i in range(20)] + [1015 + i for i in range(15)],
            'Wind Speed': [3 + i*0.1 for i in range(20)] + [2.5 + i*0.15 for i in range(15)],
            'Cloudiness': [30 + i for i in range(20)] + [25 + i for i in range(15)],
            'Weather': ['Clear' if i % 4 == 0 else 'Clouds' if i % 4 == 1 else 'Rain' if i % 4 == 2 else 'Sunny' for i in range(35)]
        })
        test_data.to_csv(test_csv, index=False)

        original_path = self.handler.csv_path
        self.handler.csv_path = test_csv

        try:
            # Load data
            df = self.handler.load_data()
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 35)

            # Get stats for London
            london_stats = self.handler.get_city_stats('London')
            self.assertIsNotNone(london_stats)
            self.assertIn('avg_temp', london_stats)
            self.assertIn('rain_days', london_stats)

            # Get stats for Paris
            paris_stats = self.handler.get_city_stats('Paris')
            self.assertIsNotNone(paris_stats)

            # Verify stats are different
            self.assertNotEqual(london_stats['avg_temp'], paris_stats['avg_temp'])

            # Train model and verify predictions work
            success = self.predictor.train_from_history(test_csv)
            self.assertTrue(success)

            # Test predictions with different conditions
            pred1 = self.predictor.predict_temperature(70, 1015, 4.0, 50)
            pred2 = self.predictor.predict_temperature(50, 1020, 2.0, 20)
            self.assertIsNotNone(pred1)
            self.assertIsNotNone(pred2)

        finally:
            self.handler.csv_path = original_path
            if os.path.exists(test_csv):
                os.remove(test_csv)
            os.rmdir(temp_dir)

if __name__ == '__main__':
    unittest.main()