import json, os, requests


def send_replies(replies):
    for r in replies:
        send_reply(r)


def send_reply(reply):
    """
    Sending response back to the user using facebook graph API
    """
    PAT = os.environ["PAT"]
    json = {"recipient": {"id": reply.sender_id}, "message": reply.build_message()}
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAT},
        headers={"Content-Type": "application/json"},
        data=json.dumps(json),
    )

    if r.status_code != 200:
        print(reply)
        print(json)
        print(r.json())
