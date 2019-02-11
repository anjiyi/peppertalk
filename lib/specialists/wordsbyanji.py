import json, random, requests
from html.parser import HTMLParser
from lib.specialists.base import PepperSpecialist
from lib.reply import ImageWithTitleReply, ImageListReply, ImageListElement


def is_preloaded(attrs):
    return any([a == ("id", "preloaded") for a in attrs])


class QuotesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.started = False
        self.data = None

    def handle_starttag(self, tag, attrs):
        if tag == "script" and is_preloaded(attrs):
            self.started = True

    def handle_endtag(self, tag):
        self.started = False

    def handle_data(self, data):
        if self.started:
            self.data = data

    def get_quotes(self):
        return json.loads(self.data) if self.data else []


def get_quotes():
    response = requests.get("https://andreq.me/words-by-anji")
    if response.status_code != 200:
        return []
    parser = QuotesParser()
    parser.feed(response.text)
    return parser.get_quotes()


def get_placeholder_reply(sender_id):
    return ImageWithTitleReply(
        sender_id=sender_id,
        image_url="https://andreq.me/images/piyomaru_pepper_talk.png",
        title="Words from Anji",
        subtitle="Wise as a pepper",
    )


class WordsByAnjiSpecialist(PepperSpecialist):
    """
    Replies with a quote from Anji, the wise pepper
    """

    def understands(self, message):
        intents = ["word from anji", "wise pepper"]
        lowercase = message.text.lower()
        return any([lowercase.find(i) >= 0 for i in intents])

    def reply(self, message):
        quotes = get_quotes()
        if not quotes:
            return [get_placeholder_reply(message.sender_id)]
        q = random.choice(quotes)
        return [
            ImageWithTitleReply(
                sender_id=message.sender_id,
                image_url="https://andreq.me/images/piyomaru_pepper_talk.png",
                title=q["data"]["context"],
                subtitle=q["data"]["word"],
            )
        ]


class PepperEnglishSpecialist(PepperSpecialist):
    """
    Replies with a quote from Anji, the wise pepper
    """

    def understands(self, message):
        intents = ["teach me a word"]
        lowercase = message.text.lower()
        return any([lowercase.find(i) >= 0 for i in intents])

    def reply(self, message):
        quotes = get_quotes()
        if not quotes:
            return [get_placeholder_reply(message.sender_id)]
        q = random.choice(quotes)
        return [
            ImageListReply(
                sender_id=message.sender_id,
                header=ImageListElement(
                    image_url="https://andreq.me/images/piyomaru_pepper_talk.png",
                    title=q["data"]["word"],
                    subtitle=q["data"]["definition"],
                ),
                children=[
                    ImageListElement(
                        image_url="https://andreq.me/images/anji_sqr.jpg",
                        title=q["data"]["context"],
                        subtitle=q["data"]["spelling"],
                    )
                ],
            )
        ]
