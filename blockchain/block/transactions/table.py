from .model import Transaction, Transactions


class TransactionTableManager:

    def __init__(self, connect):
        self.conn = connect
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                block_index INT,
                timestamp TIMESTAMP,
                sender TEXT,
                recipient TEXT,
                amount INT,
                message TEXT,
                signature TEXT
            )
        ''')
        self.conn.commit() 

    def create_transactions(self, transactions):
        return [self.create(transaction) for transaction in transactions]

    def create(self, transaction):
        self.cur.execute(
            "INSERT INTO Transactions (block_index, timestamp, sender, recipient, amount, message, signature) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                transaction.block_index,
                transaction.timestamp, 
                transaction.sender, 
                transaction.recipient,
                transaction.amount,
                transaction.message,
                transaction.signature
            )
        )
        # self.conn.commit() 

    def get_transactions_by_block_index(self, block_index):
        self.cur.execute("SELECT * FROM Transactions WHERE block_index='%s'" % block_index)
        return self._get_transactions()
   
    def get_transactions_by_sender(self, sender):
        self.cur.execute("SELECT * FROM Transactions WHERE sender='%s'" % sender)
        return self._get_transactions()

    def _get_transactions(self):
        return Transactions([self.get_transaction_by_record(record) for record in self.cur.fetchall()])

    def get_transaction_by_record(self, record):
        return Transaction.create_by_data(*record[1:])

