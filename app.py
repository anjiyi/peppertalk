from flask import Flask, request, render_template
from peppertalk import send_message, send_message_response, parse_user_message
from lib import facebook_verification
from lib.messenger_parser import MessengerRequestParser

app = Flask(__name__)


@app.route("/peppertalk", methods=["GET"])
def handle_verification():
    """
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook app
    """
    return facebook_verification.verify_webhooks(request.args)


@app.route("/preview", methods=["GET"])
def preview_test():
    message = request.args.get("message") or ""
    return render_template(
        "preview.html", message=message, reply=parse_user_message(message)
    )


@app.route("/test", methods=["GET"])
def test_suite():
    test_cases = [
        "Give me something spicy",
        "California weather",
        "meaning of pepper",
        "Hello",
        "Are you a pepper?",
        "Pepperoni",
        "Do me a Big\n favor",
        "[1231231:12312]",
        "\N{grinning face with smiling eyes}",
    ]
    responses = [
        {
            "message": t,
            "reply": parse_user_message(t),
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
    if message == None:
        send_message(sender_id, message_text="🌶️")
        return
    try:
        send_message_response(message.sender_id, parse_user_message(message.text))
    except:
        send_message(message.sender_id, message_text="🌶️")
    return "ok"


if __name__ == "__main__":
    app.run()
