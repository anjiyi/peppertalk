class Reply:
    def __init__(self, sender_id, text):
        self.sender_id = sender_id
        self.text = text

    def build_message(self):
        """
        Returns the messenger json representation of this message
        """
        pass


class TextOnlyReply(Reply):
    """
    Returns just text as a reply
    """

    def __init__(self, sender_id, text):
        super().__init__(sender_id, text)

    def build_message(self):
        return {"text": self.text}


# https://developers.facebook.com/docs/messenger-platform/send-messages/template/list
class ImageWithTitleReply(Reply):
    """
    Returns a image with title and subtitle
    """

    def __init__(self, sender_id, image_url, title, subtitle):
        super().__init__(sender_id, title)
        self.image_url = image_url
        self.title = title
        self.subtitle = subtitle

    def build_message(self):
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "elements": [
                        {
                            "title": self.title,
                            "subtitle": self.subtitle,
                            "image_url": self.image_url,
                        }
                    ],
                },
            }
        }
