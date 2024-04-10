from .block import Block, Transactions, Transaction
import datetime as date
import asyncio
import ecdsa
from hashlib import sha256


class Blockchain:

    def __init__(self, database, MAX_BLOCKS=100, GENERATION_PERIOD=10):
        self.database = database
        self.transactions_of_new_block = Transactions()
        self.MAX_BLOCKS = MAX_BLOCKS
        self.GENERATION_PERIOD = GENERATION_PERIOD
        self.is_running = False

    def create_wallet(self):
        sign = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=sha256)
        verif = sign.get_verifying_key()
        private_key = sign.to_string().hex() 
        public_key = verif.to_string().hex() 
        return private_key, public_key

    async def start(self):
        self.is_running = True
        chain_length = self.database.get_chain_length()
        if chain_length == 0:
            self.create_first_block()
        else:
            self.create_new_block()
        for _ in range(self.MAX_BLOCKS):
            await asyncio.sleep(self.GENERATION_PERIOD)
            self.create_new_block()

    def create_and_add_transaction(self, sender, recipient, amount, message, private_key):
        sign_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1, hashfunc=sha256)
        timestamp = date.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        string_data = ''.join(map(str, [timestamp, sender, recipient, amount, message]))
        transaction_hash = sign_key.sign(string_data.encode('utf-8')).hex()
        return self.add_transaction(sender, recipient, amount, message, transaction_hash)

    def add_transaction(self, sender, recipient, amount, message, transaction_hash):
        index_of_last_block = self.database.get_chain_length()
        transaction = Transaction.create_now(index_of_last_block, sender, recipient, amount, message, transaction_hash)
        self.transactions_of_new_block.add_transaction(transaction)

    def get_verification_blocks(self):
        chain_length = self.database.get_chain_length()
        return self.get_part_verification_blocks(0, chain_length)

    def get_part_verification_blocks(self, start_index, end_index):
        blocks = self.database.get_all_blocks()
        verification_blocks = [blocks[start_index]]
        for i in range(start_index, end_index):
            block = blocks[i + 1]
            if not verification_blocks[i].is_parent_block(block):
                break
            verification_blocks.append(block)
        return verification_blocks

    def create_new_block(self):
        last_block = self.database.get_last_block()
        new_block = last_block.get_child_block_by_transactions(self.transactions_of_new_block)
        self.database.create(new_block)

    def create_first_block(self):
        first_block = Block.create_now(0, '', 0, Transactions())
        self.database.create(first_block)

