import xkcd


def main():
    pass


def fetcher(user_input):
    commands = user_input.split()
    if len(commands) == 1 or commands[1] == "now":
        latest = xkcd.getLatestComic()
    elif commands[2] == "random":
        pass        

    """
    response = {
        "attatchment": {
            "type": "image",
            "payload": {
                "url":
            }
        }
    }
    """
