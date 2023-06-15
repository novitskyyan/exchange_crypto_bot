import sqlite3


class Database:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INT PRIMARY KEY,
        state TEXT,
        btc FLOAT,
        eth FLOAT,
        rub FLOAT,
        usd FLOAT )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS user_change(
                id INT PRIMARY KEY,
                crypto TEXT NULL,
                fiat TEXT NULL,
                count FLOAT NULL)""")

    def add_user(self, user_id, state_, btc_, eth_, rub_, usd_):
        sql = """INSERT INTO users (id, state, btc, eth, rub, usd) 
        VALUES (?, ?, ?, ?, ?, ?)"""
        self.cur.execute(sql, (user_id, state_, btc_, eth_, rub_, usd_))
        self.conn.commit()

    def get_btc(self, user_id):
        sql = """SELECT btc FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def set_btc(self, user_id, btc_):
        sql = """UPDATE users SET btc = ? WHERE id = ?"""
        self.cur.execute(sql, (btc_, user_id))
        return self.conn.commit()

    def get_eth(self, user_id):
        sql = """SELECT eth FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def set_eth(self, user_id, eth_):
        sql = """UPDATE users SET eth = ? WHERE id = ?"""
        self.cur.execute(sql, (eth_, user_id))
        return self.conn.commit()

    def get_rub(self, user_id):
        sql = """SELECT rub FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def get_usd(self, user_id):
        sql = """SELECT usd FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def get_state(self, user_id):
        sql = """SELECT state FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def set_state(self, user_id, state):
        sql = """UPDATE users SET state = ? WHERE id = ?"""

        self.cur.execute(sql, (state, user_id))
        self.conn.commit()

    def add_user_to_user_change(self, user_id):
        sql = """INSERT INTO user_change (id) 
                VALUES (?)"""
        self.cur.execute(sql, (user_id,))
        self.conn.commit()

    def set_crypto(self, user_id, crypto_):
        sql = """UPDATE user_change SET crypto = ? WHERE id = ?"""

        self.cur.execute(sql, (crypto_, user_id))
        self.conn.commit()

    def set_fiat(self, user_id, fiat_):
        sql = """UPDATE user_change SET fiat = ? WHERE id = ?"""

        self.cur.execute(sql, (fiat_, user_id))
        self.conn.commit()

    def set_count(self, user_id, count_):
        sql = """UPDATE user_change SET count = ? WHERE id = ?"""

        self.cur.execute(sql, (count_, user_id))
        self.conn.commit()

    def get_crypto(self, user_id):
        sql = """SELECT crypto FROM user_change WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def get_fiat(self, user_id):
        sql = """SELECT fiat FROM user_change WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def get_count(self, user_id):
        sql = """SELECT count FROM user_change WHERE id = ?"""
        self.cur.execute(sql, (user_id,))
        return self.cur.fetchone()[0]

    def set_rub(self, user_id, rub_):
        sql = """UPDATE users SET rub = ? WHERE id = ?"""

        self.cur.execute(sql, (rub_, user_id))
        self.conn.commit()

    def set_usd(self, user_id, usd_):
        sql = """UPDATE users SET usd = ? WHERE id = ?"""

        self.cur.execute(sql, (usd_, user_id))
        self.conn.commit()

    def check_user_by_id(self, user_id):
        sql = """SELECT * FROM users WHERE id = ?"""
        self.cur.execute(sql, (user_id, ))
        find_users = self.cur.fetchone()
        if find_users is None:
            return False
        return True









