from lib.specialists.base import *
from lib.reply import Reply
from lib.specialists.quotes import QuoteSpecialist
from lib.specialists.wordsbyanji import WordsByAnjiSpecialist, PepperEnglishSpecialist


class PepperReply:
    """
    Detailed replies from the pepper
    """

    def __init__(self, specialist_name, replies):
        self.specialist_name = specialist_name
        self.replies = replies


class Pepper:
    def reply(self, message):
        """
        Returns an array of replies, spicy because is a pepper 
        """
        specialists = [
            NoneMessageSpecialist(),
            EmptyMessageSpecialist(),
            QuoteSpecialist(),
            WordsByAnjiSpecialist(),
            PepperEnglishSpecialist(),
            DeprecatedSpecialist(),
            ReturnPepperSpecialist(),
        ]

        for s in specialists:
            if s.understands(message):
                return PepperReply(
                    specialist_name=type(s).__name__, replies=s.reply(message)
                )
        return []
