from Bot.models.message import Message, Callback, create_message, create_callback
import Ai.quote_creator as ai
from Bot.handlers import start_command, help_command, quote_command, add_to_love, love_command
import httpx

text_handlers = [start_command, help_command, love_command]
callback_handlers = [add_to_love]


async def convert_json(message_info: dict, client: httpx.AsyncClient) -> Message | Callback:
    if 'callback_query' in message_info:
        return await create_callback(update=message_info, client=client)
    return await create_message(message_info, client)


async def process_request(message_info: dict, client: httpx.AsyncClient):
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


