from myorm.model import Model


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
    User.create_table()
    FavQuote.create_table()