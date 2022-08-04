import json
import os

from flask import Flask, Response, request

app = Flask(__name__)

verify_token = os.getenv("VERIFY_TOKEN", None)
access_token = os.getenv("ACCESS_TOKEN", None)


@app.route("/webhook", methods=["GET"])
def webhook_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("WEBHOOK_VERIFIED")
            return Response(status=200, response=challenge)
        else:
            return Response(status=403)


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    body = json.loads(request.data.decode("utf-8"))

    if body["object"] == "page":
        return Response(status=200, response="EVENT_RECEIVED")
    else:
        return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)
