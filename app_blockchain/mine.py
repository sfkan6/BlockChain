import hashlib
import datetime as date
from app_blockchain.block import Block, create_first_block
from app_blockchain import sync
from main import self_save

NUM_ZEROS = 4


def _mine_block(data_block=""):
    node_blocks = sync.sync()
    prev_block = node_blocks[-1]

    new_block = mine(prev_block, data_block)
    self_save(new_block)


def generate_header(index, prev_hash, data, timestamp, nonce):
    return str(index) + prev_hash + data + str(timestamp) + str(nonce)


def calculate_hash(index, prev_hash, data, timestamp, nonce):
    header_string = generate_header(index, prev_hash, data, timestamp, nonce)
    sha = hashlib.sha256()
    sha.update(header_string.encode('utf-8'))
    return sha.hexdigest()


def mine(last_block, data_block):
    data_new_block = "I block #%s\n" % (int(last_block.index) + 1)

    index = int(last_block.index) + 1
    timestamp = date.datetime.now()
    data = data_new_block + data_block
    prev_hash = last_block.hash
    nonce = 0

    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
    while str(block_hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        nonce += 1
        block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

    block_data = {}
    block_data['index'] = index
    block_data['timestamp'] = timestamp
    block_data['data'] = data
    block_data['prev_hash'] = last_block.hash
    block_data['hash'] = block_hash
    block_data['nonce'] = nonce
    return Block(block_data)

if __name__ != "__main__":
    self_save(create_first_block())