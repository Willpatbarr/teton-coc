import os
import requests

LAT = 43.8866
LON = -111.6777

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_temperature(session=None) -> float:
    client = session or requests

    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY not set")

    url = (
        f"{BASE_URL}"
        f"?lat={LAT}"
        f"&lon={LON}"
        f"&appid={api_key}"
        f"&units=imperial"
    )

    response = client.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data["main"]["temp"]