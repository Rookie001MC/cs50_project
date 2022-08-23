import os
import re

import requests
from flask import Response

from scripts import weather, xkcd_fetch

verify_token = os.getenv("VERIFY_TOKEN", None)
access_token = os.getenv("ACCESS_TOKEN", None)


def main():
    print("There's nothing here ¯\_(ツ)_/¯")


def handle_message(user_id, user_message):
    if user_message["text"]:
        re_object = re.search(r"(\/[\w]+)", user_message["text"])
        user_command = re_object.group()

        match user_command:
            case "/xkcd":
                returned_message = xkcd_fetch.fetcher(user_message)
            case "/weather":
                returned_message = weather.weather_fetch(user_message)


def handle_postback(user_id, postback_event):
    pass


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
