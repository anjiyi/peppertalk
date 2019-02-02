import random
import json
from lib.reply import TextOnlyReply
from lib.specialists.base import PepperSpecialist


class QuoteSpecialist(PepperSpecialist):
    """
    Replies with spicy quotes when invoked 
    """

    def understands(self, message):
        user_text = message.text.lower()
        request_key_words = [
            "quote",
            "give me something spicy",
            "more spicy",
            "yes please",
        ]
        for w in request_key_words:
            if w in user_text:
                return True
        return False

    def get_quote(self):
        with open("quotes.json", encoding="utf-8") as f:
            quotes = json.load(f)["quotes"]

        quote = random.choice(quotes)
        return quote["quote"] + " --" + quote["author"]

    def reply(self, message):
        return [TextOnlyReply(sender_id=message.sender_id, text=self.get_quote())]
