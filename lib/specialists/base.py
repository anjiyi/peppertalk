from peppertalk import parse_user_message
from lib.reply import Reply

class PepperSpecialist:
    def understands(self, message):
        """
        Given a message, return a list of replies 
        message: not null instance of messenger_parser.Message
        """
        raise "Implement Method"

    def reply(self, message):
        """
        Given a message, return a list of replies 
        Reply: not null instance of lib.pepper.Reply
        """
        raise "Implement Method"


def pepper(sender_id):
    return Reply(sender_id, "🌶️")


class NoneMessageSpecialist(PepperSpecialist):
    """
    Replies empty list if the message is None
    """

    def understands(self, message):
        return message == None

    def reply(self, message):
        return []


class ReturnPepperSpecialist(PepperSpecialist):
    """
    Always returns a pepper
    """

    def understands(self, message):
        return True

    def reply(self, message):
        return [pepper(message.sender_id)]


class EmptyMessageSpecialist(PepperSpecialist):
    """
    Returns a pepper if the message is empty
    """

    def understands(self, message):
        return message.text.strip() == ""

    def reply(self, message):
        return [pepper(message.sender_id)]

class DeprecatedSpecialist(PepperSpecialist):
    """
    Follow the old logic to reply a message
    """

    def understands(self, message):
        return True

    def reply(self, message):
        deprecated = parse_user_message(message.text)
        sentenceDelimiter = ". "
        return [
            Reply(message.sender_id, reply)
            for reply in deprecated.split(sentenceDelimiter)
        ]
