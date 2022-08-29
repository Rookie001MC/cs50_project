import xkcd


def fetcher(user_input):
    commands = user_input.split(" ")
    print(commands)
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
            info = "Invalid comic number or subcommand!"

    if len(info) == 2:
        response = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": info[1],
                },
            },
        }
    else:
        response = {
            "text": info,
        }

    return response


def info_getter(comic):
    try:
        alt_text = comic.getAltText()
        image_url = comic.getImageLink()
    except AttributeError:
        return "An error occured, there may be a connection error, or you must have given a non-existant comic!"
    else:
        return [alt_text, image_url]


"""
if __name__ == "__main__":
    main()
"""
