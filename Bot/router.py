from Bot.models.message import Message, Callback, create_message, create_callback
from Bot.handlers import start_command, help_command, quote_command, add_to_love, love_command
import httpx

text_handlers = [start_command, help_command, love_command]
callback_handlers = [add_to_love]


"""Данный файл содержит в себе функцию разбивающую входной json на объекты класса Message или Callback"""
"""Затем происходит обработка этого объекта через Хендлеры, которые описаны в handlers.py"""
"""В зависимости от типа Callback/Message - будет вызываться нужный хендлер"""
"""В случае отправки просто текста от пользователя, бот автоматически начнет искать цитату по введеной фразе"""


async def convert_json(message_info: dict, client: httpx.AsyncClient=None) -> Message | Callback:
    """Парсер json -> Message|Callback"""
    if 'callback_query' in message_info:
        return await create_callback(update=message_info, client=client)
    return await create_message(message_info, client)


async def process_request(message_info: dict, client: httpx.AsyncClient = None):
    info: Message | Callback = await convert_json(message_info, client)
    if isinstance(info, Message):
        for handler in text_handlers:
            response = await handler(info)
            if response:
                return
        await quote_command(info)

    elif isinstance(info, Callback):
        for handler in callback_handlers:
            response = await handler(info)
            if response:
                return


