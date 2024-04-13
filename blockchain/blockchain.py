from hashlib import sha256
import asyncio, ecdsa

from .block import Block, Transactions


class Blockchain:

    def __init__(self, database, MAX_BLOCKS=100, GENERATION_PERIOD=5):
        self.database = database
        self.transactions_of_new_block = Transactions([])
        self.is_running = False
        self.MAX_BLOCKS = MAX_BLOCKS
        self.GENERATION_PERIOD = GENERATION_PERIOD

    async def start(self):
        if not self.is_running:
            self.is_running = True
            self.create_first_block()
            await self._start_block_generation()

    async def _start_block_generation(self):
        for _ in range(self.MAX_BLOCKS):
            await asyncio.sleep(self.GENERATION_PERIOD)
            self.create_new_block()

    def create_first_block(self):
        chain_length = self.database.get_chain_length()
        if chain_length == 0:
            first_block = Block.create_now(0, '', 0, self.transactions_of_new_block)
            self._create_block(first_block)
        else:
            self.create_new_block()

    def create_new_block(self):
        last_block = self.database.get_last_block()
        new_block = last_block.get_child_block_by_transactions(self.transactions_of_new_block)
        self._create_block(new_block)

    def _create_block(self, block):
        self.database.create(block)
        self.transactions_of_new_block = Transactions([])

    def create_and_get_wallet(self):
        signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=sha256)
        private_key = signing_key.to_string().hex() 
        public_key = signing_key.get_verifying_key().to_string().hex() 
        return private_key, public_key

    def create_transaction(self, transaction):
        index_of_next_block = self.database.get_chain_length()
        if index_of_next_block != transaction.block_index:
            raise Exception()
        self.transactions_of_new_block.add(transaction)

