import sqlite3 as sq


class _ORM:
    def __init__(self):
        self.conn = sq.connect('user.db')
        self.curs = self.conn.cursor()

    def add_user(self, user_id):
        self.curs.execute(f'INSERT INTO users (user_id) VALUES ({user_id})')

    def checking_state(self, track_id):
        state = self.curs.execute(f'SELECT state FROM users WHERE track_id={track_id}')
        return state
    

# Первый вариант
user_lang = 'ru'

if user_lang == 'ru':
    lang = 0
else:
    lang = 1


a = {1: ['question', ['answer-ru', 'answer-eng']]}

print(a.get(1)[1][lang])


# Второй вариант

user_lang = 'ru'

a = {1: ['question', 'answer-ru']}
b = {1: ['question', 'answer-eng']}

if user_lang == 'ru':
    lang = a
else:
    lang = b

print(lang.get(1)[1][0])