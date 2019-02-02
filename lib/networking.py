def send_replies(replies):
    for r in replies:
        send_reply(r)


def send_reply(reply):
    """
    Sending response back to the user using facebook graph API
    """
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAT},
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"recipient": {"id": reply.sender_id}, "message": reply.build_message()}
        ),
    )
