from .model import Header


class HeaderTableManager:

    def __init__(self, connect):
        self.conn = connect
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Headers (
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
        data = self.cur.fetchall()
        return [self.get_header_by_record(header_data) for header_data in data]

    def get_by_index(self, index):
        self.cur.execute("SELECT * FROM Headers WHERE id='%s'" % index)
        return self.get_header_by_record(self.cur.fetchone())

    def get_header_by_record(self, header_data):
        return Header(*header_data)



