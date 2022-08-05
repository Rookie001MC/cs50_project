import json
import os

import requests
from flask import Flask, Response, render_template, request

import global_vars
from scripts.utils import handle_message, handle_postback

app = Flask(__name__)

verify_token = global_vars.verify_token
access_token = global_vars.access_token


@app.route("/webhook", methods=["GET"])
def webhook_verify():
    """
    Webhook verification for the bot.
    https://developers.facebook.com/docs/messenger-platform/webhooks
    """

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK_VERIFIED")
            return Response(status=200, response=challenge)
        else:
            return Response(status=403)


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    """
    Handle message events sent to the bot.
    """
    body = json.loads(request.data.decode("utf-8"))

    if body["object"] == "page":
        for entry in body["entry"]:
            webhook_event = entry["messaging"][0]
            sender_psid = webhook_event["sender"]["id"]

            if webhook_event["message"]:
                handle_message(sender_psid, webhook_event["message"])
            elif webhook_event["postback"]:
                handle_postback(sender_psid, webhook_event["postback"])
        return Response(status=200, response="EVENT_RECEIVED")
    else:
        return Response(status=404)


@app.route("/profile")
def profile_setup():
    """
    Setup the bot using the Messenger Profile API.
    """

    profile_url = f"https://graph.facebook.com/v14.0/me/messenger_profile?access_token={access_token}"
    profile = {
        "data": [
            {
                "greeting": [
                    {
                        "locale": "default",
                        "text": "This is a simple Chatbot, written in Flask, for CS50 Python.",
                    },
                    {
                        "locale": "vi_VN",
                        "text": "Đây là 1 con Chatbot, được viết bằng Flask, dành cho dự án của khoá học CS50 Python.",
                    },
                ],
                "get_started": {"payload": "GET_STARTED_PAYLOAD"},
            }
        ]
    }
    try:
        r = requests.post(url=profile_url, json=profile)

        if r.status_code == 200:
            return f"<p>Successfully setup profile!</p>"
        elif r.status_code > 500:
            print(f"Request failed: {r.text}")
            return f"<p>Profile setup failed! Please check console for details.</p>"

    except requests.exceptions.ConnectionError as err:
        print(f"No connection: {err}")


# Utilities go here.

if __name__ == "__main__":
    app.run(debug=True)
