import httpx
import unittest.mock as mock
import unittest
from Ai.quote_creator import get_quote
import Ai.text_utils as tu


class TestQuoteCreator(unittest.IsolatedAsyncioTestCase):

    @mock.patch('Ai.quote_creator.open', new_callable=mock.mock_open, read_data='PROMPT: ')
    @mock.patch('Ai.quote_creator.tu.make_quote_message')
    @mock.patch('httpx.AsyncClient.post')
    async def test_quote_creator(self, mock_post, mock_creator, mock_open):
        mock_response = mock.AsyncMock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {'content': '<think>bla</think>Цитата'}
            }]
        }
        mock_post.return_value = mock_response
        mock_creator.return_value = 'готовая цитата'

        result = await get_quote('текст')

        mock_post.assert_awaited_once()
        mock_creator.assert_called_once_with("Цитата")
        self.assertEqual(result, "готовая цитата")

    @mock.patch('Ai.quote_creator.open', new_callable=mock.mock_open, read_data='PROMPT: ')
    @mock.patch('Ai.quote_creator.tu.make_quote_message')
    @mock.patch('httpx.AsyncClient.post')
    async def test_quote_creator_network_error(self, mock_post, mock_creator, mock_open):
        mock_post.side_effect = httpx.ConnectError("Connection failed")

        with self.assertRaises(httpx.ConnectError):
            await get_quote('текст')

        mock_creator.assert_not_called()

    @mock.patch('Ai.quote_creator.open', new_callable=mock.mock_open, read_data='PROMPT: ')
    @mock.patch('Ai.quote_creator.tu.make_quote_message')
    @mock.patch('httpx.AsyncClient.post')
    async def test_quote_creator_timeout(self, mock_post, mock_creator, mock_open):
        mock_post.side_effect = httpx.ReadTimeout('Connection timed out')
        assert await get_quote('текст') is None

    def test_no_quote_appearance_maker(self):
        quote = 'NO QUOTE'
        self.assertEqual(tu.make_quote_message(quote), quote)

    def test_quote_appearance_maker(self):
        quote = 'qqqq|bla bla bla'
        actual = tu.make_quote_message(quote)
        expected = 'qqqq\n\n_bla bla bla_'
        assert actual == expected

    def test_invalid_quote_appearance_maker(self):
        quote = 'qqqq-bla bla bla'
        actual = tu.make_quote_message(quote)
        assert actual is None

    def test_love_quote_maker(self):
        quote = 'qqqq\n\nbla bla bla'
        actual = tu.make_love_list_message(quote)
        assert actual == 'qqqq\n\n_bla bla bla_'


