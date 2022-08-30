import random

import xkcd
from scripts.xkcd_fetch import fetcher


def test_random(monkeypatch):
    # Sometimes looking at how they mark your problem sets actually works.
    # Idea for monkeypatching the randomizer:
    # https://github.com/cs50/problems/blob/2022/python/game/testing.py
    monkeypatch.setattr("random.randint", lambda a, b: 20)
    out_response = fetcher(f"/xkcd random")

    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getRandomComic().getImageLink()


def test_latest():
    out_response = fetcher(f"/xkcd")

    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getLatestComic().getImageLink()


def test_specific():
    comic_num = random.randint(1, xkcd.getLatestComicNum())
    out_response = fetcher(f"/xkcd {comic_num}")
    print(out_response)
    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getComic(comic_num).getImageLink()


def test_out_of_bounds():
    out_response = fetcher(f"/xkcd 9999")

    err_message = out_response["text"]

    assert err_message == "Your requested comic, number 9999, does not exist!"


def test_invalid_subcommand():
    out_response = fetcher(f"/xkcd invalid")

    err_message = out_response["text"]
    assert err_message == "Invalid comic number or subcommand!"
