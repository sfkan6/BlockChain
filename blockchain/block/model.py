import hashlib, random
from .header import Header


class Block:

    def __init__(self, header, transactions):
        self.header = header
        self.transactions = transactions
        self.hash = self.get_hash()

    def get_hash(self):
        sha = hashlib.sha256()
        sha.update(self.get_data_string().encode('utf-8'))
        return sha.hexdigest()

    def get_data_string(self):
        return self.header.get_data_string() + self.transactions.get_data_string()

    def get_child_block_by_transactions(self, transactions):
        index = int(self.header.index) + 1
        prev_hash = self.hash
        nonce = random.randint(0, 2147483648)
        return self.create_now(index, prev_hash, nonce, transactions)

    def is_parent_block(self, block):
        if self.header.prev_hash == block.hash:
            return True
        return False

    def is_child_block(self, block):
        if self.hash == block.header.prev_hash:
            return True
        return False

    @classmethod
    def create_now(cls, index, prev_hash, nonce, transactions):
        header = Header.create_now(index, prev_hash, nonce)
        return cls(header, transactions)

