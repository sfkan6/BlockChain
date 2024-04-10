import ecdsa
import datetime as date
from hashlib import sha256


class Transaction:

    def __init__(self, block_index, timestamp, sender, recipient, amount, message, transaction_hash):
        self.block_index = block_index
        self.timestamp = timestamp
        self.sender = sender 
        self.recipient = recipient
        self.amount = amount
        self.message = message
        self.transaction_hash = transaction_hash

    @property
    def is_valid(self):
        verif_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1, hashfunc=sha256)
        try:
            if verif_key.verify(self.transaction_hash, self.get_data_string):
                return True
        except:
            return False
        return False

    def get_data_string(self):
        string_data = [self.timestamp, self.sender, self.recipient, self.amount, self.message]
        return ''.join(map(str, string_data))

    def __lt__(self, transaction):
        return self.timestamp < transaction.timestamp
   
    @classmethod
    def create_now(cls, block_index, sender, recipient, amount, message, transaction_hash):
        timestamp = date.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return cls(block_index, timestamp, sender, recipient, amount, message, transaction_hash)


class Transactions:

    def __init__(self, transactions=[]):
        self.transactions = transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_sorted(self):
        return sorted(self.transactions, key=lambda transaction: transaction)
  
    def get_data_string(self):
        transaction_strings = [transaction.get_data_string() for transaction in self.transactions]
        return ''.join(map(str, transaction_strings))

    @classmethod
    def create_by_transaction_data(cls, transaction_data):
        transactions = [Transaction(*data) for data in transaction_data]
        return cls(transactions)

    def __iter__(self):
        return iter(self.transactions)
