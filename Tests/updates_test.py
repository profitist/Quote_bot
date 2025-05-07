import unittest
from unittest import mock
import httpx
from Bot.sender import *


class UpdatesTest(unittest.IsolatedAsyncioTestCase):
    @mock.patch('httpx.AsyncClient.get')
    async def test_get_updates_success(self, mock_get):
        mock_response = mock.AsyncMock()
        mock_response.json.return_value = {'result': [{'update_id': 1}]}
        mock_get.return_value = mock_response

        client = httpx.AsyncClient()
        result = await get_updates(client, offset=123)

        self.assertEqual(result, [{'update_id': 1}])
        mock_get.assert_awaited_once_with(main.BASE_URL + 'getUpdates?offset=123', timeout=10)

    @mock.patch('httpx.AsyncClient.post')
    async def test_sending_message(self, mock_post):
        client = httpx.AsyncClient()
        await send_message(client, chat_id=12345, text='Привет')

        mock_post.assert_awaited_once_with(
            main.BASE_URL + 'sendMessage',
            json={'chat_id': 12345, 'text': 'Привет', 'parse_mode': 'Markdown'}
        )

    @mock.patch('httpx.AsyncClient.post')
    async def test_sending_message_with_keyboard(self, mock_post):
        expected_keyboard = {
            "inline_keyboard": [
                [{"text": "В избранное", "callback_data": "add_love"}]
            ]
        }
        client = httpx.AsyncClient()
        await send_message_with_keyboard(client=client, chat_id=1, text='nothing')
        mock_post.assert_awaited_once_with(
            main.BASE_URL + 'sendMessage',
            json={'chat_id': 1, 'text': 'nothing', 'parse_mode': 'Markdown', 'reply_markup': expected_keyboard}
        )

    @mock.patch('httpx.AsyncClient.get')
    async def test_sending_message_with_httpxErrors(self, mock_get):
        mock_get.side_effect = httpx.NetworkError('error', request=mock.AsyncMock())
        client = httpx.AsyncClient()
        assert await get_updates(client=client, offset=123) is None



