class Message:
    def __init__(self, sender_id, recipient_id, message_type, text):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message_type = message_type
        self.text = text

    def __eq__(self, other):
        if other == None:
            return False
        return self.__dict__ == other.__dict__


class MessengerRequestParser:
    def get_message(self, json):
        if json["object"] == "page":
            for entry in json["entry"]:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        if not "text" in messaging_event["message"]:
                            return None

                        if "attachments" in messaging_event["message"]:
                            return None

                        return Message(
                            sender_id=messaging_event["sender"]["id"],
                            recipient_id=messaging_event["recipient"]["id"],
                            message_type="text",
                            text=messaging_event["message"]["text"],
                        )
        return None
