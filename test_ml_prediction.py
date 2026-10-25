"""
Unit tests for ml_prediction.py
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ml_prediction import WeatherPredictor

class TestWeatherPredictor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = WeatherPredictor()
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv_path = os.path.join(self.temp_dir, 'test_weather.csv')

        # Create sample training data
        self.sample_data = pd.DataFrame({
            'Temperature': [15.5, 16.2, 18.0, 17.5, 14.8, 19.2, 13.5, 20.1, 16.8, 17.9, 15.0, 18.5],
            'Humidity': [65, 70, 60, 55, 75, 50, 80, 45, 68, 62, 72, 58],
            'Pressure': [1013, 1015, 1020, 1018, 1010, 1022, 1008, 1025, 1016, 1019, 1012, 1021],
            'Wind Speed': [3.5, 4.0, 2.5, 3.0, 5.5, 2.0, 6.0, 1.5, 3.8, 2.8, 4.2, 2.2],
            'Cloudiness': [40, 50, 30, 20, 80, 10, 90, 5, 45, 35, 55, 25],
            'Weather': ['Clouds', 'Rain', 'Clear', 'Clear', 'Rain', 'Clear', 'Rain', 'Clear', 'Clouds', 'Clear', 'Rain', 'Clear']
        })

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)
        os.rmdir(self.temp_dir)

    def test_init(self):
        """Test initialization"""
        self.assertIsInstance(self.predictor.temp_model, type(self.predictor.temp_model))
        self.assertIsInstance(self.predictor.rain_model, type(self.predictor.rain_model))
        self.assertIsInstance(self.predictor.scaler, type(self.predictor.scaler))
        self.assertFalse(self.predictor.is_trained)

    def test_train_from_history_success(self):
        """Test successful training"""
        self.sample_data.to_csv(self.test_csv_path, index=False)

        result = self.predictor.train_from_history(self.test_csv_path)
        self.assertTrue(result)
        self.assertTrue(self.predictor.is_trained)

    def test_train_from_history_insufficient_data(self):
        """Test training with insufficient data"""
        small_data = self.sample_data.head(5)
        small_data.to_csv(self.test_csv_path, index=False)

        result = self.predictor.train_from_history(self.test_csv_path)
        self.assertFalse(result)
        self.assertFalse(self.predictor.is_trained)

    def test_train_from_history_missing_columns(self):
        """Test training with missing required columns"""
        bad_data = pd.DataFrame({
            'Temp': [15, 16, 17, 18],
            'Hum': [60, 65, 70, 75]
        })
        bad_data.to_csv(self.test_csv_path, index=False)

        result = self.predictor.train_from_history(self.test_csv_path)
        self.assertFalse(result)
        self.assertFalse(self.predictor.is_trained)

    def test_train_from_history_file_not_found(self):
        """Test training with non-existent file"""
        result = self.predictor.train_from_history('/non/existent/path.csv')
        self.assertFalse(result)
        self.assertFalse(self.predictor.is_trained)

    def test_predict_temperature_trained(self):
        """Test temperature prediction when model is trained"""
        self.sample_data.to_csv(self.test_csv_path, index=False)
        self.predictor.train_from_history(self.test_csv_path)

        prediction = self.predictor.predict_temperature(65, 1013, 3.5, 40)
        self.assertIsNotNone(prediction)
        self.assertIsInstance(prediction, float)

    def test_predict_temperature_not_trained(self):
        """Test temperature prediction when model is not trained"""
        prediction = self.predictor.predict_temperature(65, 1013, 3.5, 40)
        self.assertIsNone(prediction)

    def test_predict_rain_trained(self):
        """Test rain prediction when model is trained"""
        self.sample_data.to_csv(self.test_csv_path, index=False)
        self.predictor.train_from_history(self.test_csv_path)

        prediction, probability = self.predictor.predict_rain(65, 1013, 3.5, 40)
        self.assertIsNotNone(prediction)
        self.assertIsNotNone(probability)
        self.assertIn(prediction, [0, 1])
        self.assertGreaterEqual(probability, 0.0)
        self.assertLessEqual(probability, 100.0)

    def test_predict_rain_not_trained(self):
        """Test rain prediction when model is not trained"""
        result = self.predictor.predict_rain(65, 1013, 3.5, 40)
        self.assertIsNone(result)

    def test_get_weather_summary(self):
        """Test weather summary generation"""
        weather_data = {
            'temperature': 22.5,  # Changed to pleasant temperature range (15-25°C)
            'humidity': 70,
            'wind_speed': 12.0
        }

        summary = self.predictor.get_weather_summary(weather_data)
        self.assertIsInstance(summary, str)
        self.assertIn('सुहावना', summary)  # Should contain Hindi text for pleasant weather
        self.assertIn('नम', summary)  # Should contain humidity info
        self.assertIn('हल्की हवा', summary)  # Should contain wind info

    def test_get_weather_summary_extreme_conditions(self):
        """Test weather summary with extreme conditions"""
        # Test very cold
        cold_weather = {'temperature': -5, 'humidity': 85, 'wind_speed': 30}
        summary = self.predictor.get_weather_summary(cold_weather)
        self.assertIn('बहुत ठंडा', summary)
        self.assertIn('बहुत नम', summary)
        self.assertIn('तेज हवा', summary)

        # Test very hot
        hot_weather = {'temperature': 40, 'humidity': 20, 'wind_speed': 5}
        summary = self.predictor.get_weather_summary(hot_weather)
        self.assertIn('बहुत गर्म', summary)

if __name__ == '__main__':
    unittest.main()