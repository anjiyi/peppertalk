import os

FACEBOOK_VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]


def verify_webhooks(args):
    if args.get("hub.verify_token", "") == FACEBOOK_VERIFY_TOKEN:
        print("succefully verified")
        return args.get("hub.challenge", "")
    else:
        print("Wrong verification token!")
        return "Wrong verification token"
