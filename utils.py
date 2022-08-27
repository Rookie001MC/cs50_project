import os
import re
from time import sleep

import requests
from flask import Response

from scripts import weather, xkcd_fetch

verify_token = os.getenv("VERIFY_TOKEN", None)
access_token = os.getenv("ACCESS_TOKEN", None)


def main():
    print("There's nothing here ¯\_(ツ)_/¯")


def handle_message(user_message):
    if user_message["text"]:
        re_object = re.search(r"(\/[\w]+)", user_message["text"])
        if re_object is not None:
            user_command = re_object.group()
            full_command = user_message["text"]

            match user_command:
                case "/help":
                    returned_object = {
                        "text": f"Available commands:\n\n - /xkcd [random/latest/(any number)]: Gets a XKCD webcomic 📖. Leave blank for the latest comic.\n- /weather <city>: Show current weather for the provided city ☀️."
                    }
                case "/xkcd":
                    returned_object = xkcd_fetch.fetcher(full_command)
                case "/weather":
                    returned_object = weather.weather_fetch(full_command)
                case _:
                    returned_object = {
                        "text": "Sorry, but this command does not exist.\n¯\_(ツ)_/¯"
                    }
        else:
            returned_object = {
                "text": f"If you're trying to send me some random text, I'm sorry, cause I'm dumb.\n¯\_(ツ)_/¯"
            }

    return returned_object


def handle_postback(sender_psid, postback_event):
    payload = postback_event["payload"]

    if payload == "GET_STARTED_PAYLOAD":
        welcome_messages = [
            "Hello there! This is Rookie's CS50 Python Project - a chatbot written in Python and Flask.",
            "Currently there are 2 available commands: ",
            "- /xkcd [random/latest/(any number)]: 📖 Gets a XKCD webcomic. Leave blank for the latest comic.",
            "- /weather <city>: 🌥️ Gets the current weather of a given city. \nThe format must be (City name, Country in 2 letters.)",
            "More features will be added in the upcoming months, provided if I have more free time as I'm in the process of applying to University.",
        ]

        for message in welcome_messages:
            response = {"text": message}
            call_sendAPI(sender_psid, response)
            sleep(5)


def call_sendAPI(sender_psid, response):
    graphapi_url = (
        f"https://graph.facebook.com/v14.0/me/messages?access_token={access_token}"
    )
    payload = {
        "recipient": {
            "id": sender_psid,
        },
        "message": response,
    }

    try:
        r = requests.post(graphapi_url, json=payload)

    except requests.exceptions.HTTPError as err:
        print(f"Message failed to send: {err}")
        return Response(response=err, status=r.status_code)
    except requests.exceptions.ConnectionError as err:
        print(f"No connection: {err}")


if __name__ == "__main__":
    main()
