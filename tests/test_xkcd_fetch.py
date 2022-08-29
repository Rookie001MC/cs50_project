import random

import xkcd
from scripts.xkcd_fetch import fetcher


def test_random(monkeypatch):
    monkeypatch.setattr("random.randint", lambda a, b: 20)
    out_response = fetcher(f"/xkcd random")

    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getRandomComic().getImageLink()


def test_latest():
    out_response = fetcher(f"/xkcd")

    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getLatestComic().getImageLink()


def test_specific():
    comic_num = 646
    out_response = fetcher(f"/xkcd {comic_num}")

    image_url = out_response["attachment"]["payload"]["url"]

    assert image_url == xkcd.getComic(comic_num).getImageLink()


# def test_random():
#    random.seed(1)
#    out_response = fetcher(f"/xkcd random")
#
#    image_url = out_response["attachment"]["payload"]["url"]
#
#   assert image_url == xkcd.getRandomComic().getImageLink()


def test_out_of_bounds():
    out_response = fetcher(f"/xkcd 9999")

    err_message = out_response["text"]

    assert (
        err_message
        == "An error occured, there may be a connection error, or you must have given a non-existant comic!"
    )
