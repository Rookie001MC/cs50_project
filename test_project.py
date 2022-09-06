import json
import os

import pytest

from project import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_home_invalid_method(client):
    resp = client.post("/")
    assert resp.status_code == 405


def test_webhook_verification(client):
    verify_token = os.getenv("VERIFY_TOKEN", None)
    query_string = {
        "hub.mode": "subscribe",
        "hub.verify_token": verify_token,
        "hub.challenge": "CHALLENGE_ACCEPTED",
    }
    resp = client.get("/webhook", query_string=query_string)
    assert resp.status_code == 200
    assert b"CHALLENGE_ACCEPTED" in resp.data


def test_webhook_verify_no_data(client):
    resp = client.get("/webhook")
    assert resp.status_code == 403
    assert b"Not enough data was given in the GET request." in resp.data


def test_webhook_verify_wrong_token(client):
    verify_token = "2opqvutgp8oer45uytvgq9o8euwyro8aqgcyrwn8"
    query_string = {
        "hub.mode": "subscribe",
        "hub.verify_token": verify_token,
        "hub.challenge": "CHALLENGE_ACCEPTED",
    }
    resp = client.get("/webhook", query_string=query_string)
    assert resp.status_code == 403
    assert b"Wrong verify token." in resp.data


def test_webhook_post(client):
    body = {
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {"sender": {"id": 12230413}, "message": {"text": "Hello world!"}}
                ]
            }
        ],
    }
    resp = client.post("/webhook", data=json.dumps(body))
    assert resp.status_code == 200
    assert b"EVENT_RECEIVED" in resp.data


def test_webhook_post_no_data(client):
    body = {}
    resp = client.post("/webhook", data=json.dumps(body))
    assert resp.status_code == 400


def test_webhook_post_invalid_object(client):
    body = {"object": "invalid"}
    resp = client.post("/webhook", data=json.dumps(body))
    assert resp.status_code == 404
