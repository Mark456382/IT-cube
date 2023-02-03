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
