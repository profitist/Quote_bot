import httpx
import asyncio
from typing import Optional
import main


async def get_updates(client: httpx.AsyncClient, offset: int) -> Optional[list]:
    """Получение обновлений с пришедших сообщений телеграмм бота"""
    try:
        updates = await client.get(main.BASE_URL + f'getUpdates?offset={offset}', timeout=10)
        data_json = await updates.json()
        data = data_json.get('result', None)
        return data
    except (httpx.NetworkError, httpx.RemoteProtocolError, httpx.ConnectTimeout) as e:
        print(f'Ошибка соединения {e}, Через 3 секунды обработаю снова!')
        return None



async def send_message(client: httpx.AsyncClient, chat_id: int, text: str) -> None:
    """Функция отправки текстового сообщения"""
    url = main.BASE_URL + 'sendMessage'
    await client.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})


async def send_message_with_keyboard(client: httpx.AsyncClient, chat_id: int, text: str) -> None:
    """Функция отправки текстового сообщения с InlineKeyboard на добавление цитаты в избранное"""
    url = main.BASE_URL + 'sendMessage'
    keyboard = {
        "inline_keyboard": [
            [{"text": "В избранное", "callback_data": "add_love"}],
        ]
    }
    json_data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown', 'reply_markup': keyboard}
    await client.post(url, json=json_data)