import os
import re

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
