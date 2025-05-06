from Bot.models.message import Message, Callback
from database.models import User, FavQuote


async def register_user(message: Message):
    if User.get_or_create(user_id=message.author.tg_id):
        return None
    user = User(
        user_id=message.author.tg_id,
        username=message.author.username,
    )
    user.save()


async def save_love_quote(callback: Callback):
    user_id = callback.message.author.tg_id
    quote = callback.message.text
    fav_quote = FavQuote(user_id=user_id, quote=quote)
    fav_quote.save()


async def get_fav_quote(message: Message):
    rows = FavQuote.filter(user_id=message.author.tg_id)
    return rows
