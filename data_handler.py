"""
Data Handler Module
Manage CSV files and data operations
"""

import pandas as pd
import os

class DataHandler:
    def __init__(self):
        self.csv_path = "../weatherHistory.csv"
    
    def load_data(self):
        """Load weather history CSV"""
        try:
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                return df
            else:
                print(f"CSV file not found at {self.csv_path}")
                return None
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def get_city_stats(self, city):
        """Get statistics for a specific city"""
        df = self.load_data()
        if df is None:
            return None
        
        try:
            city_data = df[df['City'].str.lower() == city.lower()]
            
            if len(city_data) == 0:
                return None
            
            stats = {
                'avg_temp': city_data['Temperature'].mean(),
                'max_temp': city_data['Temperature'].max(),
                'min_temp': city_data['Temperature'].min(),
                'avg_humidity': city_data['Humidity'].mean(),
                'avg_wind': city_data['Wind Speed'].mean(),
                'rain_days': len(city_data[city_data['Weather'].str.contains('rain', case=False, na=False)])
            }
            
            return stats
        except Exception as e:
            print(f"Error getting stats: {e}")
            return None
    
    def save_weather_record(self, city, weather_data):
        """Save current weather to CSV"""
        try:
            record = {
                'City': city,
                'Temperature': weather_data.get('temperature', 0),
                'Humidity': weather_data.get('humidity', 0),
                'Pressure': weather_data.get('pressure', 0),
                'Wind Speed': weather_data.get('wind_speed', 0),
                'Cloudiness': weather_data.get('cloudiness', 0),
                'Weather': weather_data.get('weather', 'Unknown')
            }
            
            # Append to existing CSV or create new
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])
            
            df.to_csv(self.csv_path, index=False)
            print(f"Weather record saved for {city}")
            
        except Exception as e:
            print(f"Error saving record: {e}")
