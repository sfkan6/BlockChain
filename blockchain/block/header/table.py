from .model import Header


class HeaderTableManager:

    def __init__(self, connect):
        self.conn = connect
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Headers(
                id INT PRIMARY KEY,
                timestamp TIMESTAMP,
                prev_hash TEXT,
                nonce INT
            )
        ''')
        self.conn.commit() 

    def create(self, header):
        self.cur.execute(
            "INSERT INTO Headers (id, timestamp, prev_hash, nonce) VALUES ('%s', '%s', '%s', '%s')" % (
                header.index,
                header.timestamp, 
                header.prev_hash,
                header.nonce
            )
        )
        # self.conn.commit() 

    def get_max_index(self):
        self.cur.execute("SELECT MAX(id) FROM Headers")
        return self.cur.fetchone()[0]

    def get_all(self):
        self.cur.execute("SELECT * FROM Headers")
        return self._get_headers()

    def get_by_index(self, index):
        self.cur.execute("SELECT * FROM Headers WHERE id='%s'" % index)
        return self._get_header()

    def _get_headers(self):
        return [self.get_header_by_record(record) for record in self.cur.fetchall()]

    def _get_header(self):
        return self.get_header_by_record(self.cur.fetchone())

    def get_header_by_record(self, record):
        return Header(*record)



