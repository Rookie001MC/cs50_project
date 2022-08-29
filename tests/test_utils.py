import utils


def test_main_no_action(capfd):
    utils.main()
    out, err = capfd.readouterr()
    assert out == "There's nothing here ¯\_(ツ)_/¯\n"


def test_handle_message_command():
    request_object = {"text": "/help"}
    response = utils.handle_message(request_object)
    assert response == {
        "text": f"Available commands:\n\n - /xkcd [random/latest/(any number)]: Gets a XKCD webcomic 📖. Leave blank for the latest comic.\n- /weather <city>: Show current weather for the provided city ☀️."
    }


def test_handle_message_invalid_command():
    request_object = {"text": "/invalid"}
    response = utils.handle_message(request_object)
    assert response == {"text": "Sorry, but this command does not exist.\n¯\_(ツ)_/¯"}


def test_handle_message_deny_normal_text():
    request_object = {"text": "oooga booga"}
    response = utils.handle_message(request_object)
    assert response == {
        "text": f"If you're trying to send me some random text, I'm sorry, cause I'm dumb.\n¯\_(ツ)_/¯"
    }
