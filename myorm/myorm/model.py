import sqlite3



class Model:
    table = ''
    fields = {}


    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs.get(field))
        self.id = kwargs.get('id')  # для delete и get

    @classmethod
    def connect(cls):
        return sqlite3.connect('db.sqlite3')

    @classmethod
    def create_table(cls):
        columns = ', '.join(f"{k} {v}" for k, v in cls.fields.items())
        query = f"CREATE TABLE IF NOT EXISTS {cls.table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
        with cls.connect() as conn:
            conn.execute(query)

    def save(self):
        keys = ', '.join(self.fields.keys())
        placeholders = ', '.join(['?'] * len(self.fields))
        values = [getattr(self, k) for k in self.fields]
        query = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
        with self.connect() as conn:
            cursor = conn.execute(query, values)
            self.id = cursor.lastrowid
            conn.commit()

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.table}"
        return cls._fetch(query)

    @classmethod
    def get(cls, **kwargs):
        key, value = list(kwargs.items())[0]
        query = f"SELECT * FROM {cls.table} WHERE {key} = ? LIMIT 1"
        result = cls._fetch(query, [value])
        return result[0] if result else None

    @classmethod
    def filter(cls, **kwargs):
        conditions = ' AND '.join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        query = f"SELECT * FROM {cls.table} WHERE {conditions}"
        return cls._fetch(query, values)

    def delete(self):
        if not self.id:
            raise ValueError("Object must have 'id' to be deleted.")
        query = f"DELETE FROM {self.table} WHERE id = ?"
        with self.connect() as conn:
            conn.execute(query, [self.id])
            conn.commit()

    @classmethod
    def _fetch(cls, query, params=[]):
        with cls.connect() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    @classmethod
    def get_or_create(cls, **kwargs):
        """Получает пользователя или создает нового, если его нет."""
        user = cls.get(user_id=kwargs['user_id'])
        if not user:
            user = cls(**kwargs)
            user.save()
        return user
