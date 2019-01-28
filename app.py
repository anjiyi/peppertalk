from flask import Flask, request, render_template
from lib import facebook_verification
from lib.messenger_parser import MessengerRequestParser
from lib.message import Message
from lib.pepper import Pepper
from lib.networking import send_replies

app = Flask(__name__)


@app.route("/peppertalk", methods=["GET"])
def handle_verification():
    """
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook app
    """
    return facebook_verification.verify_webhooks(request.args)


def test_message(text):
    return Message("<SENDER_ID>", "<RECIPIENT_ID>", "text", text)


def extract_text_replies(text):
    return "".join([reply.text for reply in Pepper().reply(test_message(text))])


@app.route("/preview", methods=["GET"])
def preview_test():
    """
    Custom pepper query UI to make it easier to test the pepper
    """
    message = request.args.get("message") or ""
    return render_template(
        "preview.html", message=message, reply=extract_text_replies(message)
    )


@app.route("/test", methods=["GET"])
def test_suite():
    """
    Renders a list of queries to verify that the pepper works properly
    """
    test_cases = [
        "Give me something spicy",
        "meaning of pepper",
        "Hello",
        "Are you a pepper?",
        "",
        "Do me a Big\n favor",
        "[1231231:12312]",
        "\N{grinning face with smiling eyes}",
    ]
    responses = [
        {
            "message": t,
            "reply": extract_text_replies(t),
            "view": {"class": "odd" if index % 2 else "even"},
        }
        for index, t in enumerate(test_cases)
    ]
    return render_template("test_suite.html", responses=responses)


@app.route("/peppertalk", methods=["POST"])
def handle_message():
    """
    Handle messages sent by facebook messenger to the applicaiton
    """
    messenger_parser = MessengerRequestParser()
    message = messenger_parser.get_message(request.get_json())
    replies = Pepper().reply(message)
    send_replies(replies)
    return "ok"


if __name__ == "__main__":
    app.run()
