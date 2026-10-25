"""
Pytest configuration and shared fixtures
"""

import pytest
import os
import tempfile
import pandas as pd

@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing"""
    return pd.DataFrame({
        'City': ['London', 'London', 'Paris', 'Paris', 'Berlin'],
        'Temperature': [15.5, 16.2, 18.0, 17.5, 20.1],
        'Humidity': [65, 70, 60, 55, 45],
        'Pressure': [1013, 1015, 1020, 1018, 1025],
        'Wind Speed': [3.5, 4.0, 2.5, 3.0, 1.5],
        'Cloudiness': [40, 50, 30, 20, 5],
        'Weather': ['Clouds', 'Rain', 'Clear', 'Clear', 'Clear']
    })

@pytest.fixture
def temp_csv_file(sample_weather_data):
    """Create a temporary CSV file with sample data"""
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, 'weather.csv')
    sample_weather_data.to_csv(csv_path, index=False)

    yield csv_path

    # Cleanup
    if os.path.exists(csv_path):
        os.remove(csv_path)
    os.rmdir(temp_dir)