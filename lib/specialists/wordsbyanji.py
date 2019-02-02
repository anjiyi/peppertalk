from lib.specialists.base import PepperSpecialist
from lib.reply import ImageWithTitleReply


class WordsByAnjiSpecialist(PepperSpecialist):
    """
    Replies with a quote from Anji, the wise pepper
    """

    def understands(self, message):
        intents = ["word from anji", "wise pepper"]
        lowercase = message.text.lower()
        return any([lowercase.find(i) >= 0 for i in intents])

    def reply(self, message):
        return [
            ImageWithTitleReply(
                sender_id=message.sender_id,
                image_url="https://andreq.me/words-by-anji/piyomaru.png",
                title="Words from Anji",
                subtitle="Wise as a pepper",
            )
        ]
