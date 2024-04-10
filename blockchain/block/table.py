from .header import HeaderManager
from .transactions import TransactionManager
from .model import Block


class BlockManager:

    def __init__(self, connect):
        self.header_manager = HeaderManager(connect)
        self.transaction_manager = TransactionManager(connect)

    def get_chain_length(self):
        max_index = self.header_manager.get_max_index()
        if max_index == None:
            return 0
        return int(max_index) + 1

    def create(self, block):
        self.header_manager.create(block.header)
        self.transaction_manager.create_transactions(block.transactions.get_sorted())

    def get_last_block(self):
        max_index = self.header_manager.get_max_index()
        return self.get_by_index(max_index)

    def get_all(self):
        headers = self.header_manager.get_all()
        return [self.get_block_by_header(header) for header in headers]

    def get_by_index(self, index):
        header = self.header_manager.get_by_index(index)
        return self.get_block_by_header(header)

    def get_block_by_header(self, header):
        transactions = self.get_transactions_by_block_index(header.index)
        return Block(header, transactions)

    def get_transactions_by_block_index(self, block_index):
        return self.transaction_manager.get_transactions_by_block_index(block_index)


