"""
Weather Dashboard - Desktop Application
Real-time weather with ML predictions using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from weather_api import WeatherAPI
from ml_prediction import WeatherPredictor
import os
from datetime import datetime

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Weather Dashboard")
        self.root.geometry("900x650")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize API and ML
        try:
            self.api = WeatherAPI()
            self.predictor = WeatherPredictor()
            self._train_model()
        except Exception as e:
            messagebox.showerror("Error", f"Initialization failed: {e}")
            return
        
        self.setup_ui()
    
    def _train_model(self):
        """Train ML model from historical data"""
        base_dir = os.path.dirname(__file__)
        csv_path = os.path.normpath(os.path.join(base_dir, '..', 'weatherHistory.csv', 'weatherHistory.csv'))
        if os.path.exists(csv_path):
            self.predictor.train_from_history(csv_path)
    
    def setup_ui(self):
        """Create the dashboard UI"""
        # Header
        header = tk.Frame(self.root, bg='#2d2d2d', height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header, text="🌤️ Weather Dashboard", 
                               font=('Arial', 24, 'bold'), 
                               bg='#2d2d2d', fg='#4da6ff')
        title_label.pack(pady=10)
        
        # Search Frame
        search_frame = tk.Frame(self.root, bg='#1e1e1e')
        search_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(search_frame, text="🏙️ City:", font=('Arial', 12), 
                bg='#1e1e1e', fg='white').pack(side=tk.LEFT)
        
        self.city_entry = tk.Entry(search_frame, font=('Arial', 12), width=30)
        self.city_entry.pack(side=tk.LEFT, padx=10)
        self.city_entry.insert(0, "Delhi")
        
        search_btn = tk.Button(search_frame, text="Search", 
                              command=self.search_weather,
                              bg='#4da6ff', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5)
        search_btn.pack(side=tk.LEFT)
        
        # Main Content (Tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current Weather Tab
        self.current_tab = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(self.current_tab, text="Current Weather")
        self.setup_current_weather_tab()
        
        # Predictions Tab
        self.prediction_tab = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(self.prediction_tab, text="ML Predictions")
        self.setup_prediction_tab()
        
        # Forecast Tab
        self.forecast_tab = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(self.forecast_tab, text="Forecast")
        self.setup_forecast_tab()
        
        # Initial search
        self.search_weather()
    
    def setup_current_weather_tab(self):
        """Current weather display"""
        self.current_weather_label = tk.Label(self.current_tab, 
                                             font=('Arial', 40, 'bold'),
                                             bg='#1e1e1e', fg='#4da6ff')
        self.current_weather_label.pack(pady=20)
        
        # Weather details grid
        details_frame = tk.Frame(self.current_tab, bg='#2d2d2d')
        details_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.weather_details = {}
        details = [
            ('🌡️ Temperature', 'temperature'),
            ('💧 Humidity', 'humidity'),
            ('🌬️ Wind Speed', 'wind_speed'),
            ('☁️ Cloudiness', 'cloudiness'),
            ('🌍 Weather', 'weather'),
            ('⚙️ Pressure', 'pressure')
        ]
        
        for i, (label, key) in enumerate(details):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(details_frame, bg='#32323f', relief=tk.RAISED)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Label(frame, text=label, font=('Arial', 12, 'bold'),
                    bg='#32323f', fg='#4da6ff').pack(pady=5)
            
            self.weather_details[key] = tk.Label(frame, text='--',
                                               font=('Arial', 14),
                                               bg='#32323f', fg='white')
            self.weather_details[key].pack(pady=5)
        
        # Summary
        self.summary_label = tk.Label(self.current_tab, 
                                     font=('Arial', 11),
                                     bg='#1e1e1e', fg='#ffcc00',
                                     wraplength=800, justify=tk.CENTER)
        self.summary_label.pack(pady=15)
    
    def setup_prediction_tab(self):
        """ML Predictions display"""
        pred_frame = tk.Frame(self.prediction_tab, bg='#2d2d2d', relief=tk.RAISED)
        pred_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(pred_frame, text="🤖 ML Weather Predictions", 
                font=('Arial', 14, 'bold'),
                bg='#2d2d2d', fg='#4da6ff').pack(pady=10)
        
        self.temp_pred_label = tk.Label(pred_frame, font=('Arial', 12),
                                       bg='#2d2d2d', fg='white')
        self.temp_pred_label.pack(pady=10)
        
        self.rain_pred_label = tk.Label(pred_frame, font=('Arial', 12),
                                       bg='#2d2d2d', fg='white')
        self.rain_pred_label.pack(pady=10)
        
        self.pred_status = tk.Label(pred_frame, font=('Arial', 10),
                                   bg='#2d2d2d', fg='#ffcc00')
        self.pred_status.pack(pady=20)
    
    def setup_forecast_tab(self):
        """Forecast display"""
        self.forecast_text = tk.Text(self.forecast_tab, 
                                    font=('Arial', 10),
                                    bg='#2d2d2d', fg='white',
                                    height=20, width=80)
        self.forecast_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def search_weather(self):
        """Fetch weather and update UI"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        # Run in separate thread to avoid freezing
        thread = threading.Thread(target=self._fetch_and_update, args=(city,))
        thread.daemon = True
        thread.start()
    
    def _fetch_and_update(self, city):
        """Fetch weather data and update UI"""
        # Current weather
        weather = self.api.get_current_weather(city)
        
        if 'error' in weather:
            self.root.after(0, lambda: messagebox.showerror("Error", weather['error']))
            return
        
        # Update current weather tab
        self.root.after(0, self._update_current_weather, weather)
        
        # Predictions
        self.root.after(0, self._update_predictions, weather)
        
        # Forecast
        forecast = self.api.get_forecast(city)
        self.root.after(0, self._update_forecast, forecast)
    
    def _update_current_weather(self, weather):
        """Update current weather display"""
        self.current_weather_label.config(
            text=f"{weather['city']}, {weather['country']}"
        )
        
        self.weather_details['temperature'].config(
            text=f"{weather['temperature']}°C"
        )
        self.weather_details['humidity'].config(
            text=f"{weather['humidity']}%"
        )
        self.weather_details['wind_speed'].config(
            text=f"{weather['wind_speed']} m/s"
        )
        self.weather_details['cloudiness'].config(
            text=f"{weather['cloudiness']}%"
        )
        self.weather_details['weather'].config(
            text=weather['description'].capitalize()
        )
        self.weather_details['pressure'].config(
            text=f"{weather['pressure']} hPa"
        )
        
        summary = self.predictor.get_weather_summary(weather)
        self.summary_label.config(text=summary)
    
    def _update_predictions(self, weather):
        """Update ML predictions"""
        if not self.predictor.is_trained:
            self.pred_status.config(text="⚠️ ML Model: Training data not available")
            self.temp_pred_label.config(text="Temperature Prediction: N/A")
            self.rain_pred_label.config(text="Rain Prediction: N/A")
            return
        
        temp_pred = self.predictor.predict_temperature(
            weather['humidity'], weather['pressure'],
            weather['wind_speed'], weather['cloudiness']
        )
        
        rain_pred = self.predictor.predict_rain(
            weather['humidity'], weather['pressure'],
            weather['wind_speed'], weather['cloudiness']
        )
        
        if temp_pred:
            self.temp_pred_label.config(
                text=f"🌡️ Next Temperature: {temp_pred}°C"
            )
        
        if rain_pred:
            will_rain, prob = rain_pred
            status = "☔ Will Rain" if will_rain else "☀️ No Rain"
            self.rain_pred_label.config(
                text=f"{status} (Probability: {prob}%)"
            )
        
        self.pred_status.config(text="✅ Predictions updated")
    
    def _update_forecast(self, forecast):
        """Update forecast display"""
        self.forecast_text.config(state=tk.NORMAL)
        self.forecast_text.delete('1.0', tk.END)
        
        if not forecast:
            self.forecast_text.insert(tk.END, "No forecast data available")
            self.forecast_text.config(state=tk.DISABLED)
            return
        
        text = "📅 5-Day Forecast\n" + "="*70 + "\n\n"
        
        for item in forecast:
            text += f"📍 {item['timestamp']}\n"
            text += f"   🌡️ Temperature: {item['temperature']}°C\n"
            text += f"   ☁️ Weather: {item['weather']}\n"
            text += f"   💧 Humidity: {item['humidity']}%\n"
            text += f"   🌬️ Wind: {item['wind_speed']} m/s\n"
            text += f"   ☔ Rain Prob: {item['rain_probability']}%\n"
            text += "-" * 70 + "\n"
        
        self.forecast_text.insert(tk.END, text)
        self.forecast_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
