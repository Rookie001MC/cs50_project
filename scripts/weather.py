import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv("../.env")
global api_key
api_key = os.getenv("WEATHER_API_KEY", None)


def main():
    print(f"API Key: {api_key}")
    print(weather_fetch(input("Enter city: ").strip()))


def weather_fetch(city):
    """Fetches the current weather of an user-inputted city.

    Args:
        city (string): City name, in the format of (City name, Country in 2
        letters.)

    Returns:
        string: A formatted message of the current weather of given city.
    """

    coords = city_coords_fetch(city)

    if coords is False:
        return "City does not exist!"
    elif coords == "Err-Wrong-Format":
        return "Invalid format! Must be (City name-Country in 2 letters)"

    lat, lon = coords
    city_name, weather_emoji, temp, humidity, wind_speed, weather = call_weather_api(
        lat, lon
    )

    message = f"""Showing temperature for {city_name}:

Today's weather is {weather_emoji}\t{weather}, with temperatures at {round(temp)} degrees Celcius.

Wind speeds is {wind_speed} km/h.
Humidity is {humidity}%."""
    return message


def city_coords_fetch(city):
    """Fetches the coordinates of an user-inputted city.

    As stated in OWM's documentation, built-in geocoding (which returns the weather
    using only the city name), will be deprecated soon.

    In order to prevent any future breakages, I built this function to search
    the given city, and return its corresponding coordinates, which will be
    needed for the weather fetching.

    This also does the necessary sanity check (Checks for the syntax of the
    inputted city.)

    Args:
        city (str): City name, in the format of (City name, Country in 2
        letters.)

    Raises:
        ValueError: When the inputted city does not match the format.
        AttributeError: When there is no result.

    Returns:
        list: Contains the latitude and longitude of the inputted city.
    """
    try:
        print(city)
        city_name, country = city.split(",")
        print(f"{city_name}\t{country}")
    except ValueError:
        return "Err-Wrong-Format"
    GEO_API = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "appid": api_key,
        "q": f"{city_name.strip()}, {country.strip()}",
    }

    r = requests.get(GEO_API, params=geo_params)

    response = r.json()

    if len(response) == 0:
        return False
    else:
        print(response)
        result = response[
            0
        ]  # Since we asked the user to input the city based on the syntax, we only need the first one.
        lat = round(float(result["lat"]), 2)
        lon = round(float(result["lon"]), 2)

    return [lat, lon]


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


def call_weather_api(lat, lon):
    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    api_params = {"appid": api_key, "lat": lat, "lon": lon, "units": "metric"}
    r = requests.get(API_URL, params=api_params)

    response = r.json()

    city_name = f"{response['name']}, {response['sys']['country']}"
    weather_id = int(response["weather"][0]["id"])
    weather_emoji = get_weather_emoji(weather_id)
    data_nums = response["main"]
    temp = data_nums["temp"]
    humidity = data_nums["humidity"]
    wind_speed = response["wind"]["speed"]
    weather = response["weather"][0]["description"]

    data = [city_name, weather_emoji, temp, humidity, wind_speed, weather]

    return data


if __name__ == "__main__":
    main()
