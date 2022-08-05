import global_vars
import requests
from flask import Response

verify_token = global_vars.verify_token
access_token = global_vars.access_token


def main():
    print("There's nothing here ¯\_(ツ)_/¯")


def handle_message(user_id, user_message):
    pass


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
        "message": {
            "text": response,
        },
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
