import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from Bot.models.message import Message, Callback, User, Chat
import Bot.models.message as parser


class TestParseData(unittest.IsolatedAsyncioTestCase):
    async def test_create_message_without_name_fields(self):
        data = {
            'message': {
                'message_id': 123,
                'from': {
                    'id': 111,
                    'username': 'anon_user'
                },
                'chat': {
                    'id': 222,
                    'username': 'anon_user'
                },
                'date': 1746608123,
                'text': 'без имени'
            }
        }

        mock_client = AsyncMock()
        user = User(111, 'anon_user')
        chat = Chat(222)
        expected = Message(123, 'без имени', user, chat, mock_client)

        actual = await parser.create_message(data, mock_client)

        self.assertEqual(actual.author.first_name, None)
        self.assertEqual(actual.author.last_name, None)
        self.assertEqual(actual.text, expected.text)
        self.assertEqual(actual.client, mock_client)

    async def test_parse_message_info(self):
        data = {
            'update_id': 335873652,
            'message': {
                'message_id': 416,
                'from': {
                    'id': 886989682,
                    'first_name': 'Ivan',
                    'last_name': 'Mikhaylov',
                    'username': 'profitist'
                },
                'chat': {
                    'id': 886989682,
                    'first_name': 'Ivan',
                    'last_name': 'Mikhaylov',
                    'username': 'profitist'
                },
                'date': 1746608123,
                'text': 'гордость'
            }
        }

        mock_client = AsyncMock()
        actual_user = User(886989682, 'profitist', 'Ivan', 'Mikhaylov')
        chat = Chat(886989682)
        expected = Message(416, 'гордость', actual_user, chat, mock_client)

        actual = await parser.create_message(data, mock_client)

        self.assertEqual(actual.id, expected.id)
        self.assertEqual(actual.text, expected.text)
        self.assertEqual(actual.author.tg_id, expected.author.tg_id)
        self.assertEqual(actual.chat.chat_id, expected.chat.chat_id)
        self.assertEqual(actual.client, expected.client)

    async def test_create_callback(self):
        data = {
            "callback_query": {
                "id": "abc123",
                "data": "clicked!",
                "from": {
                    "id": 999,
                    "username": "tester",
                    "first_name": "Test",
                    "last_name": "User"
                },
                "message": {
                    "message_id": 555,
                    "from": {
                        "id": 999,
                        "username": "tester",
                        "first_name": "Test",
                        "last_name": "User"
                    },
                    "chat": {
                        "id": 999,
                        "username": "tester"
                    },
                    "text": "original message",
                    "date": 1746608123
                }
            }
        }

        mock_client = AsyncMock()

        callback = await parser.create_callback(data, mock_client)

        self.assertEqual(callback.id, "abc123")
        self.assertEqual(callback.data, "clicked!")
        self.assertEqual(callback.message.text, "original message")
        self.assertEqual(callback.client, mock_client)

    async def test_create_message_with_invalid_user(self):
        data = {
            "callback_query": {
                "id": "abc123",
                "data": "clicked!",
                "from": {
                    "id": 999,
                    "username": "tester",
                },
                "message": {
                    "message_id": 555,
                    "from": {
                        "id": 999,
                        "username": "tester",
                    },
                    "chat": {
                        "id": 999,
                    },
                    "text": "original message",
                    "date": 1746608123
                }
            }
        }

        mock_client = AsyncMock()
        callback = await parser.create_callback(data, mock_client)
        self.assertEqual(callback.id, "abc123")
        self.assertEqual(callback.data, "clicked!")
        self.assertEqual(callback.message.text, "original message")
        self.assertEqual(callback.client, mock_client)

    async def test_create_message_with_invalid_data(self):
        data = {'message': None}
        mock_client = AsyncMock()
        actual = await parser.create_message(data, mock_client)
        assert actual is None


