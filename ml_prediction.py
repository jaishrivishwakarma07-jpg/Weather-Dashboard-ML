"""
Machine Learning Prediction Module
Predict temperature, rain probability, and weather patterns
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import os

class WeatherPredictor:
    def __init__(self):
        self.temp_model = LinearRegression()
        self.rain_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train_from_history(self, csv_path):
        """
        Train models using historical weather data
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Prepare features
            if len(df) < 10:
                print("Not enough data to train models")
                return False
            
            # Features: humidity, pressure, wind_speed, cloudiness
            feature_cols = ['Humidity', 'Pressure', 'Wind Speed', 'Cloudiness']
            available_cols = [col for col in feature_cols if col in df.columns]
            
            if not available_cols:
                print("Required columns not found in CSV")
                return False
            
            X = df[available_cols].fillna(0).values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Temperature prediction (Linear Regression)
            if 'Temperature' in df.columns:
                y_temp = df['Temperature'].fillna(0).values
                self.temp_model.fit(X_scaled, y_temp)
            
            # Rain prediction (Classification)
            if 'Weather' in df.columns:
                y_rain = (df['Weather'].str.lower().str.contains('rain|drizzle|thunderstorm', na=False)).astype(int).values
                if len(np.unique(y_rain)) > 1:
                    self.rain_model.fit(X_scaled, y_rain)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict_temperature(self, humidity, pressure, wind_speed, cloudiness):
        """
        Predict next temperature based on current conditions
        """
        if not self.is_trained:
            return None
        
        try:
            features = np.array([[humidity, pressure, wind_speed, cloudiness]])
            features_scaled = self.scaler.transform(features)
            prediction = self.temp_model.predict(features_scaled)[0]
            return round(prediction, 1)
        except:
            return None
    
    def predict_rain(self, humidity, pressure, wind_speed, cloudiness):
        """
        Predict if it will rain (0 = No, 1 = Yes)
        """
        if not self.is_trained:
            return None
        
        try:
            features = np.array([[humidity, pressure, wind_speed, cloudiness]])
            features_scaled = self.scaler.transform(features)
            prediction = self.rain_model.predict(features_scaled)[0]
            probability = self.rain_model.predict_proba(features_scaled)[0][1] * 100
            return int(prediction), round(probability, 1)
        except:
            return None
    
    def get_weather_summary(self, current_weather):
        """
        Generate AI-based weather analysis
        """
        temp = current_weather.get('temperature', 0)
        humidity = current_weather.get('humidity', 0)
        wind = current_weather.get('wind_speed', 0)
        
        summary = []
        
        # Temperature analysis
        if temp < 0:
            summary.append(f"❄️ बहुत ठंडा ({temp}°C) - घर में रहें")
        elif temp < 15:
            summary.append(f"🧊 ठंडा ({temp}°C) - गरम कपड़े पहनें")
        elif temp < 25:
            summary.append(f"😊 सुहावना ({temp}°C) - बाहर जाने का सही समय")
        elif temp < 35:
            summary.append(f"☀️ गर्म ({temp}°C) - धूप में सावधानी रखें")
        else:
            summary.append(f"🔥 बहुत गर्म ({temp}°C) - ठंडे रहें")
        
        # Humidity analysis
        if humidity > 80:
            summary.append(f"💧 बहुत नम ({humidity}%)")
        elif humidity > 60:
            summary.append(f"🌤️ नम ({humidity}%)")
        
        # Wind analysis
        if wind > 25:
            summary.append(f"💨 तेज हवा ({wind} m/s)")
        elif wind > 10:
            summary.append(f"🌬️ हल्की हवा ({wind} m/s)")
        
        return " | ".join(summary)
