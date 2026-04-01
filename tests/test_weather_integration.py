import os
import pytest
from weather.client import get_weather_temperature
# Skip this test if the WEATHER_API_KEY is not present in the environment
# random comment to update the title of the workflow run
pytestmark = pytest.mark.skipif(
    "WEATHER_API_KEY" not in os.environ,
    reason="WEATHER_API_KEY not set"
)

def test_get_weather_real_api():
    temp = get_weather_temperature()
    assert isinstance(temp, (int, float))