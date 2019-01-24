from flask import Flask, request, render_template
from peppertalk import send_message, send_message_response, parse_user_message
from lib import facebook_verification

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
    q = request.args.get("query") or ""
    return render_template("preview.html", query=q, answer=parse_user_message(q))


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
            "query": t,
            "answer": parse_user_message(t),
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
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    try:
                        message_text = messaging_event["message"]["text"]
                        send_message_response(
                            sender_id, parse_user_message(message_text)
                        )
                    except:
                        send_message(sender_id, message_text="🌶️")

    return "ok"


if __name__ == "__main__":
    app.run()
