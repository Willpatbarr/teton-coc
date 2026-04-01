import os
from weather.client import get_weather_temperature, LAT, LON, BASE_URL

def test_get_weather_with_requests_mock(requests_mock):
    os.environ["WEATHER_API_KEY"] = "FAKE"

    expected_url = (
        f"{BASE_URL}"
        f"?lat={LAT}"
        f"&lon={LON}"
        f"&appid=FAKE"
        f"&units=imperial"
    )

    requests_mock.get(
        expected_url,
        json={"main": {"temp": 72}},
        status_code=200
    )

    temp = get_weather_temperature()
    assert temp == 72
