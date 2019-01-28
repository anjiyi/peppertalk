from lib.specialists.base import *
from lib.reply import Reply
from lib.specialists.quotes import QuoteSpecialist


class Pepper:
    def reply(self, message):
        """
        Returns an array of replies, spicy because is a pepper 
        """
        specialists = [
            NoneMessageSpecialist(),
            EmptyMessageSpecialist(),
            QuoteSpecialist(),
            DeprecatedSpecialist(),
            ReturnPepperSpecialist(),
        ]

        for s in specialists:
            if s.understands(message):
                return s.reply(message)
        return []
