import xkcd


def main():
    pass


def fetcher(user_input):
    commands = user_input.split()

    if len(commands) == 1 or commands[1] == "latest":
        latest = xkcd.getLatestComic()
        info = info_getter(latest)
    elif commands[1] == "random":
        random = xkcd.getRandomComic()
        info = info_getter(random)
    else:
        try:
            specific = xkcd.getComic(int(commands[1]))
            info = info_getter(specific)
        except ValueError:
            return "Invalid comic number or subcommand!"

    response = {
        "text": info[0],
        "attachment": {
            "type": "image",
            "payload": {
                "url": info[1],
                "is_resuable": True,
            },
        },
    }
    return response


def info_getter(comic):
    try:
        alt_text = comic.getAltText()
        image_url = comic.getImageLink()
    except AttributeError:
        return "An error occured, there may be a connection error, or you must have given a non-existant comic!"

    return [alt_text, image_url]


"""
if __name__ == "__main__":
    main()
"""
