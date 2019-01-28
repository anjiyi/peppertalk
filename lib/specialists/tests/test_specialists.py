from unittest import TestCase
from lib.specialists.base import *
from lib.messenger_parser import Message
from lib.pepper import Reply


class TestEmptyMessageSpecialist(TestCase):
    def test_accept_empty_message(self):
        specialist = EmptyMessageSpecialist()
        self.assertEqual(
            specialist.understands(
                Message(
                    sender_id="<SENDER_ID>",
                    recipient_id="<RECIPIENT_ID>",
                    message_type="text",
                    text="",
                )
            ),
            True,
        )

    def test_accept_blank_message(self):
        specialist = EmptyMessageSpecialist()
        self.assertEqual(
            specialist.understands(
                Message(
                    sender_id="<SENDER_ID>",
                    recipient_id="<RECIPIENT_ID>",
                    message_type="text",
                    text="     ",
                )
            ),
            True,
        )
