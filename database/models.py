from myorm.model import Model
"""Модели для работы с БД"""


class User(Model):
    table = 'users'
    fields = {
        'user_id': 'INT',
        'username': 'VARCHAR(40)',
    }


class FavQuote(Model):
    table = 'fav_quotes'
    fields = {
        'user_id': 'INT',
        'quote': 'VARCHAR(400)',
    }


def init_db():
    """Запуск БД"""
    User.create_table()
    FavQuote.create_table()