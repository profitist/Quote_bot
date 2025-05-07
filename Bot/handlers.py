from Bot.models.message import Message, Callback
import Bot.sender as sender
from database import requests as rq
import Ai.quote_creator
import Ai.text_utils as text_utils


def query_handler(callback_data: str):
    """Декоратор на обработку указанной команды"""
    def decorator(func):
        async def wrapper(callback: Callback):
            if callback.data == callback_data:
                return await func(callback)
            return None
        return wrapper
    return decorator


def command_handler(command: str):
    """Декоратор на обработку Коллбэков"""
    def decorator(func):
        async def wrapper(message: Message):
            text = message.text
            if text.startswith(f"/{command}"):
                return await func(message)
            return None
        return wrapper
    return decorator


"""Обработчики команд"""


@command_handler('start')
async def start_command(message: Message) -> bool:
    text = f'Привет {message.author.username}! Я цитатник'
    await rq.register_user(message)
    await sender.send_message(message.client, chat_id=message.chat.chat_id, text=text)
    return True


@command_handler('help')
async def help_command(message: Message) -> bool:
    text = ('Вот краткая справка обо мне: Я умею искать цитаты известных людей по кодовому слову!\n'
            'Все, что тебе нужно - написать команду /quote {Твоя тема цитаты}\n\n'
             'Вот другой список команд которые помогут тебе разобраться с работой со мной\n'
             '/about - Пришлю информацию о моем создателе\n'
             '/love - Покажу список твоих любимых цитат\n')
    await sender.send_message(message.client, chat_id=message.chat.chat_id, text=text)
    return True


async def quote_command(message: Message) -> bool:
    if len(message.text) <= 3:
        await sender.send_message(message.client, chat_id=message.chat.chat_id, text='Введите тему цитаты корректно')
        return True
    await sender.send_message(message.client, chat_id=message.chat.chat_id, text='Ожидайте, идет поиск цитаты...')
    quote = await Ai.quote_creator.get_quote(message.text)
    if quote and quote != 'NO QUOTE':
        await sender.send_message_with_keyboard(message.client, chat_id=message.chat.chat_id, text=quote)
    elif quote == 'NO QUOTE':
        await sender.send_message(message.client, chat_id=message.chat.chat_id, text='Цитата с таким словом не найдена')
    else:
        answer_text = 'Упс, цитаты временно недоступны, попробуйте позже'
        await sender.send_message(message.client, chat_id=message.chat.chat_id, text=answer_text)
    return True


@command_handler('love')
async def love_command(message: Message) -> bool:
    print("Обработка love")
    rows = await rq.get_fav_quote(message)
    print(rows[0])
    message_text = '\n\n\n'.join(text_utils.make_love_list_message(row['quote']) for row in rows)
    await sender.send_message(message.client, chat_id=message.chat.chat_id, text=message_text)
    return True


@query_handler('add_love')
async def add_to_love(callback: Callback) -> bool:
    await rq.save_love_quote(callback)
    await sender.send_message(
        callback.message.client, chat_id=callback.message.chat.chat_id, text='Добавлено в избраноое')
    return True
