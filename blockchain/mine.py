import hashlib
import datetime as date
from blockchain.block import Block
from settings import datab


NUM_ZEROS = 4


def verification(chain):
    l_chain = len(chain)
    if l_chain > 1:
        blockchain = []
        i = 0
        blockchain.append(Block(chain[i]))
        while i < l_chain - 1:
            blockchain.append(Block(chain[i + 1]))
            if blockchain[i].create_self_hash() != blockchain[i + 1].prev_hash:
                return []
            i += 1
    return chain


def generate_header(index, timestamp, prev_hash, data, nonce):
    return str(index) + str(timestamp) + prev_hash + data + str(nonce)


def calculate_hash(index, prev_hash, data, timestamp, nonce):
    header_string = generate_header(index, timestamp, prev_hash, data, nonce)
    sha = hashlib.sha256()
    sha.update(header_string.encode('utf-8'))
    return sha.hexdigest()


def mine(data_block=''):
    new_block = _mine(Block(datab.get_last()), data_block)
    datab.create(new_block)


def _mine(last_block, data_block):

    index = int(last_block.index) + 1
    data_new_block = "I block #%s\n" % (index)

    timestamp = date.datetime.now()
    data = data_new_block + data_block
    prev_hash = last_block.hash
    nonce = 0
    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

    while block_hash[0:NUM_ZEROS] != '0' * NUM_ZEROS:
        nonce += 1
        block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

    block = (index, timestamp, last_block.hash, block_hash, data, nonce)
    return Block(block)


def create_first_block():
    block = {}
    block['index'] = 0
    block['timestamp'] = date.datetime.now()
    block['data'] = 'First block data'
    block['prev_hash'] = ''
    block['nonce'] = 0
    return datab.create(Block(block))

