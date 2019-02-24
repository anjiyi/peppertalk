import json, sys
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
    pepper_reply = Pepper().reply(test_message(text))
    return ([reply for reply in pepper_reply.replies], pepper_reply.specialist_name)


@app.route("/preview", methods=["GET"])
def preview_test():
    """
    Custom pepper query UI to make it easier to test the pepper
    """
    message = request.args.get("message") or ""
    replies, specialist_name = extract_text_replies(message)
    return render_template(
        "preview.html",
        specialist_name=specialist_name,
        message=message,
        reply="\n".join([r.text for r in replies]),
        json=[r.build_message() for r in replies],
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
        "be wise",
        "teach me a word",
        "\N{grinning face with smiling eyes}",
    ]
    replies = [extract_text_replies(t) for t in test_cases]
    responses = [
        {
            "message": test_cases[index],
            "specialist_name": specialist_name,
            "reply": " ".join([r.text for r in rs]),
            "json": [r.build_message() for r in rs],
            "view": {"class": "odd" if index % 2 else "even"},
        }
        for index, (rs, specialist_name) in enumerate(replies)
    ]
    return render_template("test_suite.html", responses=responses)


@app.template_filter("get_hash")
def get_hash(data):
    return "id" + str(hash(data))


@app.template_filter("json_stringify")
def json_stringify(blob):
    return json.dumps(blob, indent=2)


@app.route("/peppertalk", methods=["POST"])
def handle_message():
    """
    Handle messages sent by facebook messenger to the applicaiton
    """
    debug = request.args.get("debug")
    messenger_parser = MessengerRequestParser()
    message = messenger_parser.get_message(request.get_json())
    try:
        pepper_reply = Pepper().reply(message)
        send_replies(pepper_reply.replies)
    except Exception:
        if debug:
            raise sys.exc_info()[1]
        print(sys.exc_info())
    return "ok"


def get_test_client():
    return app.test_client()


if __name__ == "__main__":
    app.run()
