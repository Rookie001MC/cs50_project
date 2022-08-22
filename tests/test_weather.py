import json
import os

import pytest
import requests
from scripts.weather import call_weather_api, city_coords_fetch

TEST_LOCATIONS = [
    ["Tay Ninh, VN", 11.3, 106.1],
    ["Amsterdam, NL", 52.37, 4.89],
    ["Washington D.C., US", 38.9, -77.04],
]


def test_default():
    input = TEST_LOCATIONS[0]
    assert call_weather_api(input[1], input[2]) == generate_result(input[1], input[2])


def test_different_country():
    input = TEST_LOCATIONS[1]
    assert call_weather_api(input[1], input[2]) == generate_result(input[1], input[2])


def test_city_coords():
    input = TEST_LOCATIONS[2]
    assert city_coords_fetch(input[0]) == [input[1], input[2]]


def test_wrong_city_format():
    input = "literally just a random string here lmao"
    assert city_coords_fetch(input) == "Err-Wrong-Format"


def test_no_city():
    input = "another random string here, too"
    assert city_coords_fetch(input) == False


def generate_result(lat, lon):

    api_key = os.getenv("WEATHER_API_KEY", None)
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_params = {"appid": api_key, "lat": lat, "lon": lon, "units": "metric"}

    response = requests.get(base_url, params=api_params)
    x = response.json()
    if x["cod"] != "404":

        city_name = f"{x['name']}, {x['sys']['country']}"

        y = x["main"]

        temp = y["temp"]
        humidity = y["humidity"]
        wind_speed = x["wind"]["speed"]

        z = x["weather"]

        weather = z[0]["description"]
        weather_id = z[0]["id"]

        weather_emoji = get_weather_emoji(weather_id)

        data = [city_name, weather_emoji, temp, humidity, wind_speed, weather]
        return data
    else:
        return False


def get_weather_emoji(weather_id):
    """Returns the emoji corresponding to the weather ID.
    A list of the weather ID can be found here:
    https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

    Args:
        weather_id (int): The weather ID received from the OWM API.

    Returns:
        str: An emoji corresponding to the weather ID.
    """
    # Weather ID reference:
    THUNDERSTORM = range(200, 300)
    DRIZZLE = range(300, 400)
    RAIN = range(500, 600)
    SNOW = range(600, 700)
    ATMOSPHERE = range(700, 800)
    CLEAR = range(800, 801)
    CLOUDY = range(801, 900)

    if weather_id in THUNDERSTORM:
        emoji = "⛈️"
    elif weather_id in DRIZZLE:
        emoji = "💧"
    elif weather_id in RAIN:
        emoji = "🌧️"
    elif weather_id in SNOW:
        emoji = "❄️"
    elif weather_id in ATMOSPHERE:
        emoji = "🌀"
    elif weather_id in CLEAR:
        emoji = "☀️"
    elif weather_id in CLOUDY:
        emoji = "☁️"
    else:
        emoji = "🌈"

    return emoji
