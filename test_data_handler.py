"""
Unit tests for data_handler.py
"""

import unittest
import pandas as pd
import os
import tempfile
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_handler import DataHandler

class TestDataHandler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.handler = DataHandler()
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv_path = os.path.join(self.temp_dir, 'test_weather.csv')

        # Create sample data
        self.sample_data = pd.DataFrame({
            'City': ['London', 'London', 'Paris', 'Paris'],
            'Temperature': [15.5, 16.2, 18.0, 17.5],
            'Humidity': [65, 70, 60, 55],
            'Pressure': [1013, 1015, 1020, 1018],
            'Wind Speed': [3.5, 4.0, 2.5, 3.0],
            'Cloudiness': [40, 50, 30, 20],
            'Weather': ['Clouds', 'Rain', 'Clear', 'Rain']
        })

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temp files
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)
        os.rmdir(self.temp_dir)

    def test_load_data_file_exists(self):
        """Test loading data when file exists"""
        self.sample_data.to_csv(self.test_csv_path, index=False)

        # Temporarily change csv_path
        original_path = self.handler.csv_path
        self.handler.csv_path = self.test_csv_path

        try:
            df = self.handler.load_data()
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 4)
            self.assertListEqual(list(df.columns), list(self.sample_data.columns))
        finally:
            self.handler.csv_path = original_path

    def test_load_data_file_not_exists(self):
        """Test loading data when file does not exist"""
        # Temporarily change csv_path to non-existent file
        original_path = self.handler.csv_path
        self.handler.csv_path = '/non/existent/path.csv'

        try:
            df = self.handler.load_data()
            self.assertIsNone(df)
        finally:
            self.handler.csv_path = original_path

    def test_get_city_stats_success(self):
        """Test getting city statistics successfully"""
        self.sample_data.to_csv(self.test_csv_path, index=False)

        original_path = self.handler.csv_path
        self.handler.csv_path = self.test_csv_path

        try:
            stats = self.handler.get_city_stats('London')
            self.assertIsNotNone(stats)
            self.assertAlmostEqual(stats['avg_temp'], 15.85, places=2)
            self.assertEqual(stats['max_temp'], 16.2)
            self.assertEqual(stats['min_temp'], 15.5)
            self.assertEqual(stats['avg_humidity'], 67.5)
            self.assertEqual(stats['avg_wind'], 3.75)
            self.assertEqual(stats['rain_days'], 1)  # One 'Rain' entry
        finally:
            self.handler.csv_path = original_path

    def test_get_city_stats_city_not_found(self):
        """Test getting stats for non-existent city"""
        self.sample_data.to_csv(self.test_csv_path, index=False)

        original_path = self.handler.csv_path
        self.handler.csv_path = self.test_csv_path

        try:
            stats = self.handler.get_city_stats('Tokyo')
            self.assertIsNone(stats)
        finally:
            self.handler.csv_path = original_path

    def test_get_city_stats_no_data(self):
        """Test getting stats when no data file exists"""
        original_path = self.handler.csv_path
        self.handler.csv_path = '/non/existent/path.csv'

        try:
            stats = self.handler.get_city_stats('London')
            self.assertIsNone(stats)
        finally:
            self.handler.csv_path = original_path

    def test_save_weather_record_new_file(self):
        """Test saving weather record to new file"""
        original_path = self.handler.csv_path
        self.handler.csv_path = self.test_csv_path

        weather_data = {
            'temperature': 20.5,
            'humidity': 75,
            'pressure': 1010,
            'wind_speed': 5.0,
            'cloudiness': 25,
            'weather': 'Clear'
        }

        try:
            self.handler.save_weather_record('Berlin', weather_data)

            # Check if file was created and data saved
            self.assertTrue(os.path.exists(self.test_csv_path))
            df = pd.read_csv(self.test_csv_path)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]['City'], 'Berlin')
            self.assertEqual(df.iloc[0]['Temperature'], 20.5)
            self.assertEqual(df.iloc[0]['Weather'], 'Clear')
        finally:
            self.handler.csv_path = original_path

    def test_save_weather_record_append(self):
        """Test appending weather record to existing file"""
        self.sample_data.to_csv(self.test_csv_path, index=False)

        original_path = self.handler.csv_path
        self.handler.csv_path = self.test_csv_path

        weather_data = {
            'temperature': 22.0,
            'humidity': 80,
            'pressure': 1005,
            'wind_speed': 6.0,
            'cloudiness': 10,
            'weather': 'Sunny'
        }

        try:
            self.handler.save_weather_record('Berlin', weather_data)

            # Check if record was appended
            df = pd.read_csv(self.test_csv_path)
            self.assertEqual(len(df), 5)  # Original 4 + 1 new
            last_row = df.iloc[-1]
            self.assertEqual(last_row['City'], 'Berlin')
            self.assertEqual(last_row['Temperature'], 22.0)
        finally:
            self.handler.csv_path = original_path

if __name__ == '__main__':
    unittest.main()