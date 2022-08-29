import xkcd


def fetcher(user_input):
    """Process the inputted command and fetches the requested comic.

    Args:
        user_input (str): the command as inputted by user.

    Returns:
        dict: a response object to be sent back to the `handle_message` function for processing and sending to FB.
    """
    commands = user_input.split(" ")
    print(commands)
    if len(commands) == 1 or commands[1] == "latest":
        latest = xkcd.getLatestComic()
        comic_url = get_image_url(latest)
    elif commands[1] == "random":
        random = xkcd.getRandomComic()
        comic_url = get_image_url(random)
    else:
        try:
            specific = xkcd.getComic(int(commands[1]))
            comic_url = get_image_url(specific)
        except ValueError:
            comic_url = "Invalid comic number or subcommand!"

    if comic_url:
        response = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": comic_url,
                },
            },
        }
    else:
        response = {
            "text": comic_url,
        }

    return response


def get_image_url(comic):
    """Fetches the image of a given comic.

    Args:
        comic (object): An `xkcd.Comic` object as requested by the user.

    Returns:
        str: The url of the comic.
    """
    try:
        image_url = comic.getImageLink()
    except AttributeError:
        return "An error occured, there may be a connection error, or you must have given a non-existant comic!"
    else:
        return image_url


"""
if __name__ == "__main__":
    main()
"""
