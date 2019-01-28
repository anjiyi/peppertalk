from unittest import TestCase
from lib.messenger_parser import MessengerRequestParser
from lib.message import Message


class TestMessengerParser(TestCase):
    def test_text_message(self):
        parser = MessengerRequestParser()
        json = {
            "object": "page",
            "entry": [
                {
                    "id": "<PAGE_ID>",
                    "time": 1458692752478,
                    "messaging": [
                        {
                            "sender": {"id": "<PSID>"},
                            "recipient": {"id": "<PAGE_ID>"},
                            "timestamp": 1458692752478,
                            "message": {
                                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                                "text": "hello, world!",
                                "quick_reply": {
                                    "payload": "<DEVELOPER_DEFINED_PAYLOAD>"
                                },
                            },
                        }
                    ],
                }
            ],
        }
        message = Message(
            sender_id="<PSID>",
            recipient_id="<PAGE_ID>",
            message_type="text",
            text="hello, world!",
        )

        self.assertEqual(parser.get_message(json), message)

    def test_message_with_attachment(self):
        parser = MessengerRequestParser()
        json = {
            "object": "page",
            "entry": [
                {
                    "id": "<PAGE_ID>",
                    "time": 1458692752478,
                    "messaging": [
                        {
                            "sender": {"id": "<PSID>"},
                            "recipient": {"id": "<PAGE_ID>"},
                            "timestamp": 1458692752478,
                            "message": {
                                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                                "seq": "52181",
                                "attachments": [
                                    {
                                        "type": "<image|video|audio|file>",
                                        "payload": {"url": "<ATTACHMENT_URL>"},
                                    }
                                ],
                            },
                        }
                    ],
                }
            ],
        }
        message = Message(
            sender_id="<PSID>", recipient_id="<PAGE_ID>", message_type="text", text=""
        )

        self.assertEqual(parser.get_message(json), message)

    def test_message_with_fallback_attachment(self):
        parser = MessengerRequestParser()
        json = {
            "object": "page",
            "entry": [
                {
                    "id": "<PAGE_ID>",
                    "time": 1458692752478,
                    "messaging": [
                        {
                            "sender": {"id": "<PSID>"},
                            "recipient": {"id": "<PAGE_ID>"},
                            "timestamp": 1458692752478,
                            "message": {
                                "mid": "mid.1458696618141:b4ef9d19ec21086067",
                                "text": "<URL_SENT_BY_THE_USER>",
                                "attachments": [
                                    {
                                        "type": "fallback",
                                        "payload": None,
                                        "title": "<TITLE_OF_THE_URL_ATTACHMENT>",
                                        "URL": "<URL_OF_THE_ATTACHMENT>",
                                    }
                                ],
                            },
                        }
                    ],
                }
            ],
        }
        message = Message(
            sender_id="<PSID>",
            recipient_id="<PAGE_ID>",
            message_type="text",
            text="<URL_SENT_BY_THE_USER>",
        )

        self.assertEqual(parser.get_message(json), message)
