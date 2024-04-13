from ecdsa.util import sigdecode_der
from hashlib import sha256
import ecdsa


class Transaction:

    def __init__(self, block_index, timestamp, sender, recipient, amount, message, signature):
        self.block_index = block_index
        self.timestamp = timestamp
        self.sender = sender 
        self.recipient = recipient
        self.amount = amount
        self.message = message
        self.signature = signature

    @property
    def is_valid(self):
        try:
            verifying_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1, hashfunc=sha256)
            if verifying_key.verify(bytes.fromhex(self.signature), self.get_data_string().encode(), sigdecode=sigdecode_der):
                return True
        except:
            return False
        return False

    def get_full_data_string(self):
        string_data = [self.block_index, self.timestamp, self.sender, self.recipient, self.amount, self.message, self.signature]
        return self.get_string_by_data(string_data)

    def get_data_string(self):
        string_data = [self.block_index, self.timestamp, self.sender, self.recipient, self.amount, self.message]
        return self.get_string_by_data(string_data)

    def get_string_by_data(self, data):
        return ''.join(map(str, data))

    def __lt__(self, transaction):
        return self.timestamp < transaction.timestamp

    @classmethod
    def create_by_data(cls, block_index, timestamp, sender, recipient, amount, message, signature, **kwargs):
        return Transaction(block_index, timestamp, sender, recipient, amount, message, signature)


class Transactions:

    def __init__(self, transactions: list):
        self.transactions = transactions
    
    @property
    def length(self):
        return len(self.transactions)

    def add(self, transaction):
        self.transactions.append(transaction)

    def get_sorted(self):
        return sorted(self.transactions, key=lambda transaction: transaction)
  
    def get_data_string(self):
        transaction_strings = [transaction.get_full_data_string() for transaction in self.transactions]
        return ''.join(map(str, transaction_strings))

    def get_by_id(self, transaction_id):
        return self.transactions[transaction_id]

    def __iter__(self):
        return iter(self.transactions)
