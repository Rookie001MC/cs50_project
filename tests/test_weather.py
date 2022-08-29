import datetime
import os

import requests
from scripts.weather import call_weather_api, city_coords_fetch, weather_fetch

TEST_CASES = [
    ["Tay Ninh, VN", 11.3, 106.1],
    ["Amsterdam, NL", 52.374, 4.8897],
    ["Washington D.C., US", 38.8950368, -77.0365427],
    ["/weather London, GB", -0.1257, 51.5085],
]


def test_with_slash_commands():
    input = TEST_CASES[3]
    res_object = weather_fetch(input[0])
    message = res_object["text"]
    assert message == generate_final_message(input[0])


def test_invalid_city_format_with_slash_commands():
    input = "/weather wfjioawiopnvoirwnveraiourgvbaesvesiaobaesiorbnverpioubnv"
    res_object = weather_fetch(input)
    message = res_object["text"]
    assert message == "Invalid format! Must be (City name-Country in 2 letters)"


def test_no_city_found_with_slash_commands():
    input = "/weather injfaopsenmfi, fe"
    res_object = weather_fetch(input)
    message = res_object["text"]
    assert message == "City does not exist!"


#  Annoyingly, the data changes so much that it sometimes invalidates everything else.
def test_data():
    input = TEST_CASES[0]
    assert call_weather_api(input[1], input[2]) == generate_data(input[0])


def test_data_different_country():
    input = TEST_CASES[1]
    assert call_weather_api(input[1], input[2]) == generate_data(input[0])


def test_city_coords():
    input = TEST_CASES[2]
    assert city_coords_fetch(input[0]) == [input[1], input[2]]


def test_wrong_city_format():
    input = "literally just a random string here lmao"
    assert city_coords_fetch(input) == "Err-Wrong-Format"


def test_no_city():
    input = "another random string here, too"
    assert city_coords_fetch(input) == False


# Testing utilities
def generate_data(city):
    """Another implementation for fetching data from OpenWeathermap.
    https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    """
    global api_key
    api_key = os.getenv("WEATHER_API_KEY", None)
    if "/" in city:
        command_args = city.split(" ", 1)
        city = command_args[1]
    coords = generate_geocords(city)
    if coords is False:
        return False
    else:
        lat = coords[0]
        lon = coords[1]
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_params = {"appid": api_key, "lat": lat, "lon": lon, "units": "metric"}
    response = requests.get(base_url, params=api_params)
    x = response.json()
    if x["cod"] != "404":

        city_name = f"{x['name']}, {x['sys']['country']}"

        y = x["main"]

        temp = round(y["temp"])
        humidity = y["humidity"]
        wind_speed = round(x["wind"]["speed"], 1)

        z = x["weather"]

        weather = z[0]["description"]
        weather_id = z[0]["id"]

        timezone = f"{get_date(x['timezone'])}"

        weather_emoji = get_weather_emoji(weather_id)

        data = [city_name, weather_emoji, temp, humidity, wind_speed, weather, timezone]
        return data
    else:
        return False


def get_weather_emoji(weather_id):
    """Returns an emoji corresponding to the weather ID.
    Reference code: https://realpython.com/build-a-python-weather-app-cli/#format-weather-types-in-different-colors
    Weather ID Reference: https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
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


def generate_final_message(city):
    data = generate_data(city)
    if data is False:
        return data
    city_name, weather_emoji, temp, humidity, wind_speed, weather, timezone = data

    message = f"""Showing the weather for {city_name}:

Local time: {timezone}.

Current weather is {weather_emoji} {weather}, with a temperature of {round(temp)}⁰C.

Wind speed is {wind_speed} km/h.
Humidity is {humidity}%"""
    return message


def generate_geocords(city):
    city_name, country = city.split(",")
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
        result = response[0]
        lat = float(result["lat"])
        lon = float(result["lon"])

    return [lat, lon]


def get_date(timezone):
    tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
    return datetime.datetime.now(tz=tz).strftime(
        "%d/%m/%Y, %H:%M"
    )  # strftime is just for visually formatting the datetime object
