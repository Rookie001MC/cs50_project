import xkcd


def fetcher(user_input):
    """Process the inputted command and fetches the requested comic.

    Args:
        user_input (str): the command as inputted by user.

    Returns:
        dict: a response object to be sent back to the `handle_message` function for processing and sending to FB.
    """
    commands = user_input.split(" ")
    found = True
    if len(commands) == 1:
        comic_url = xkcd.getLatestComic().getImageLink()

    elif len(commands) == 2:
        subcommand = commands[1]
        if subcommand == "latest":
            comic_url = xkcd.getLatestComic().getImageLink()

        elif subcommand == "random":
            comic_url = xkcd.getRandomComic().getImageLink()

        else:
            try:
                input_comic_num = int(subcommand)
            except ValueError:
                comic_url = "Invalid comic number or subcommand!"
                found = False
            else:
                if 1 <= input_comic_num <= xkcd.getLatestComicNum():
                    comic_url = xkcd.getComic(input_comic_num).getImageLink()
                else:
                    comic_url = f"Your requested comic, number {input_comic_num}, does not exist!"
                    found = False

    elif len(commands) > 2:
        comic_url = "Too many arguments!"
        found = False

    if found is True:
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


"""
if __name__ == "__main__":
    main()
"""
