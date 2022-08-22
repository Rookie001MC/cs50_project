import random

import pytest
import xkcd
from scripts.xkcd_fetch import fetcher


def test_random(monkeypatch):
    # Need to figure out how to test randomized functions.
    random.seed = lambda x: 10
    out_response = fetcher(f"/xkcd random")

    alt_text = out_response["text"]
    image_url = out_response["attachment"]["payload"]["url"]

    assert alt_text == xkcd.getRandomComic().getAltText()
    assert image_url == xkcd.getRandomComic().getImageLink()


def test_latest():
    out_response = fetcher(f"/xkcd")

    alt_text = out_response["text"]
    image_url = out_response["attachment"]["payload"]["url"]

    assert alt_text == xkcd.getLatestComic().getAltText()
    assert image_url == xkcd.getLatestComic().getImageLink()


def test_specific():
    comic_num = 646
    out_response = fetcher(f"/xkcd {comic_num}")

    alt_text = out_response["text"]
    image_url = out_response["attachment"]["payload"]["url"]

    assert alt_text == xkcd.getComic(comic_num).getAltText()
    assert image_url == xkcd.getComic(comic_num).getImageLink()


def test_random():
    random.seed(1)
    out_response = fetcher(f"/xkcd random")

    alt_text = out_response["text"]
    image_url = out_response["attachment"]["payload"]["url"]

    assert alt_text == xkcd.getRandomComic().getAltText()
    assert image_url == xkcd.getRandomComic().getImageLink()


def test_out_of_bounds():
    out_response = fetcher(f"/xkcd 9999")

    err_message = out_response["text"]

    assert (
        err_message
        == "An error occured, there may be a connection error, or you must have given a non-existant comic!"
    )
