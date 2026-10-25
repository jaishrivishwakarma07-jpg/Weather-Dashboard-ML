
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Weather Dashboard")
st.write("Check real-time weather for any city.")

api_key = os.getenv("WEATHER_API_KEY")

city = st.text_input("Enter City Name", "Satna")

if st.button("Get Weather"):
    if not api_key:
        st.error("WEATHER_API_KEY is missing from the root .env file.")
    elif not city.strip():
        st.warning("Please enter a city name.")
    else:
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city.strip(),
                    "appid": api_key,
                    "units": "metric"
                },
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()

                st.subheader(
                    f"{data['name']}, {data['sys']['country']}"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Temperature",
                    f"{data['main']['temp']} °C"
                )
                col2.metric(
                    "Humidity",
                    f"{data['main']['humidity']}%"
                )
                col3.metric(
                    "Wind Speed",
                    f"{data.get('wind', {}).get('speed', 0)} m/s"
                )

                st.write(
                    "**Weather:**",
                    data["weather"][0]["description"].title()
                )
                st.write(
                    "**Pressure:**",
                    f"{data['main']['pressure']} hPa"
                )
                st.success("Live weather loaded successfully!")

            elif response.status_code == 404:
                st.error("City not found. Check the spelling.")
            elif response.status_code == 401:
                st.error("API key invalid or not activated.")
            else:
                st.error(f"Weather API error: {response.status_code}")

        except requests.RequestException as error:
            st.error(f"Network error: {error}")
