from lib.message import Message


class MessengerRequestParser:
    def get_message(self, json):
        if json["object"] == "page":
            for entry in json["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        text = ""
                        if "text" in messaging_event["message"]:
                            text = messaging_event["message"]["text"]

                        return Message(
                            sender_id=messaging_event["sender"]["id"],
                            recipient_id=messaging_event["recipient"]["id"],
                            message_type="text",
                            text=text,
                        )
        return None
