from unittest import TestCase
from lib.specialists.wordsbyanji import WordsByAnjiSpecialist
from lib.reply import Reply
from lib.message import Message


class TestWordsByAnjiSpecialist(TestCase):
    def test_doesnt_understands_message(self):
        specialist = WordsByAnjiSpecialist()
        self.assertEqual(
            specialist.understands(
                Message(
                    sender_id="<SENDER_ID>",
                    recipient_id="<RECIPIENT_ID>",
                    message_type="text",
                    text="are you a pepper?",
                )
            ),
            False,
        )

    def test_understands_message(self):
        specialist = WordsByAnjiSpecialist()
        self.assertEqual(
            specialist.understands(
                Message(
                    sender_id="<SENDER_ID>",
                    recipient_id="<RECIPIENT_ID>",
                    message_type="text",
                    text="give me a word from anji",
                )
            ),
            True,
        )

        self.assertEqual(
            specialist.understands(
                Message(
                    sender_id="<SENDER_ID>",
                    recipient_id="<RECIPIENT_ID>",
                    message_type="text",
                    text="wise pepper",
                )
            ),
            True,
        )
