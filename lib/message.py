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
