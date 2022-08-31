import hashlib
import datetime as date


class Block(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

        if not hasattr(self, 'nonce'):
            self.nonce = 'None'
        if not hasattr(self, 'hash'):
            self.hash = self.create_self_hash()

    def header_string(self):
        return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)

    def create_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        return sha.hexdigest()

    def __dict__(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['data'] = str(self.data)
        info['nonce'] = str(self.nonce)
        return info

    def __str__(self):
        return "Block<prev_hash: %s,hash: %s>" % (self.prev_hash, self.hash)


def verification(f_chain):
    if len(f_chain) > 1:
        chain = []
        for i in f_chain:
            block_data = {}
            block_data['index'] = i[0]
            block_data['timestamp'] = i[1]
            block_data['prev_hash'] = i[2]
            block_data['hash'] = i[3]
            block_data['data'] = i[4]
            block_data['nonce'] = i[5]
            chain.append(Block(block_data))
        for i in range(len(chain) - 1):
            if chain[i].create_self_hash() != chain[i + 1].prev_hash:
                return []
    return f_chain


def create_first_block():
    block_data = {}
    block_data['index'] = 0
    block_data['timestamp'] = date.datetime.now()
    block_data['data'] = 'First block data'
    block_data['prev_hash'] = ''
    block_data['nonce'] = 0
    return Block(block_data)
