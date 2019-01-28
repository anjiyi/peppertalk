def send_replies(replies):
    for r in replies:
        send_reply(r.sender_id, r.text)


def send_reply(sender_id, message_text):
    """
    Sending response back to the user using facebook graph API
    """
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAT},
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"recipient": {"id": sender_id}, "message": {"text": message_text}}
        ),
    )
