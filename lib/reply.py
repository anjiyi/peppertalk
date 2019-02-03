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


# https://developers.facebook.com/docs/messenger-platform/send-messages/template
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
                    "template_type": "generic",
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


class ImageListElement:
    """
    Element of a image list, contains img, title and subtitle
    """

    def __init__(self, title, subtitle, image_url):
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url

    def build_element(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "image_url": self.image_url,
        }


class ImageListReply(Reply):
    """
    Returns a list composed of a header and elements
    Args:
    sender_id: int
    header: ImageListElement
    children: List[ImageListElement]
    """

    def __init__(self, sender_id, header, children):
        super().__init__(sender_id, header.title)
        self.header = header
        self.children = children

    def build_message(self):
        elements = [self.header.build_element()]
        for c in self.children:
            elements.append(c.build_element())
        return {
            "attachment": {
                "type": "template",
                "payload": {"template_type": "generic", "elements": elements},
            }
        }
