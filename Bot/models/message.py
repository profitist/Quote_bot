import httpx


class User:
    def __init__(self, tg_id: int, username: str, first_name: str = None, last_name: str = None):
        self.tg_id = tg_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class Chat:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id


class Message:
    def __init__(self, message_id: int, text: str, author: User, chat: Chat, client: httpx.AsyncClient):
        self.text = text
        self.author = author
        self.chat = chat
        self.id = message_id
        self.client = client


class Callback:
    def __init__(
        self,
        callback_id: str,
        data: str,
        message: Message,
        client: httpx.AsyncClient,
    ):
        self.id = callback_id
        self.data = data
        self.message = message
        self.client = client


async def create_message(message_json: dict, client: httpx.AsyncClient) -> Message | None:
    info = message_json.get('message', None)
    if info is None:
        return None
    message_id = info['message_id']
    message_from_info = info['from']
    print(message_from_info)
    try:
        user = User(
            message_from_info['id'],
            message_from_info['username'],
            message_from_info['first_name'],
            message_from_info['last_name'])
    except KeyError:
        user = User(message_from_info['id'], message_from_info['username'])
    chat = Chat(info['chat']['id'])
    text = info['text']
    print(user.tg_id)
    return Message(message_id, text, user, chat, client)


async def create_callback(update: dict, client: httpx.AsyncClient) -> Callback:
    print(update)
    cb = update["callback_query"]
    msg = await create_callback_message(cb, client)
    callback = Callback(
        callback_id=cb["id"],
        data=cb["data"],
        message=msg,
        client=client
    )
    print('callback created')
    print(callback.message.author.tg_id)
    return callback


async def create_callback_message(callback: dict, client: httpx.AsyncClient) -> Message:
    print(callback)
    # message_id = callback['message_id']
    message_from_info = callback['from']
    bot_message = await create_message(callback, client)
    try:
        user = User(
            message_from_info['id'],
            message_from_info['username'],
            message_from_info['first_name'],
            message_from_info['last_name'])
    except KeyError:
        user = User(message_from_info['id'], message_from_info['username'])
    chat = Chat(bot_message.chat.chat_id)
    text = bot_message.text
    print(user.tg_id)
    return Message(1, text, user, chat, client)



