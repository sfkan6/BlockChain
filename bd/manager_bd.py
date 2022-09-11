import sqlite3


class DataB:
    def __init__(self):
        self.conn, self.cur = self.connect()

    def connect(self):
        conn = sqlite3.connect('DataChain.db')
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS DataChain (
                id INT PRIMARY KEY,
                timestamp TIMESTAMP,
                prev_hash TEXT,
                hash TEXT,
                data TEXT,
                nonce INT
            )
        ''')
        conn.commit() 
        return conn, cur

    def create(self, block):
        self.cur.execute(
            "INSERT INTO DataChain (id, timestamp, prev_hash, hash, data, nonce) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                block.index,
                block.timestamp, 
                block.prev_hash,
                block.hash,
                block.data,
                block.nonce
            )
        )

    def get_all(self):
        self.cur.execute("SELECT * FROM DataChain")
        return self.cur.fetchall()

    def get_block(self, index):
        self.cur.execute("SELECT * FROM DataChain WHERE id='%s'" % index)
        return self.cur.fetchone()

    def get_last(self):
        index = self.len_chain()
        index = 0 if index == 0 else index - 1
        return self.get_block(index)

    def get_data_block(self, index):
        self.cur.execute("SELECT data FROM DataChain WHERE id='%s'" % index)
        return self.cur.fetchone()[0]

    def len_chain(self):
        self.cur.execute("SELECT MAX(id) FROM DataChain")
        l = self.cur.fetchone()[0]
        length = l + 1 if l else 0
        return length

