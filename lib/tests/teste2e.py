from unittest import TestCase
import requests


class TestE2E(TestCase):
    def test_it_doesnt_throw(self):
        response = requests.post(
            "http://127.0.0.1:5000/peppertalk?debug=1",
            json={
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
            },
        )
        if response.status_code != 200:
            print(response.text)
            self.assertEqual(response, True)
