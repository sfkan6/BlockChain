import hashlib


class Block(object):
    def __init__(self, dictionary):
        if isinstance(dictionary, list) or isinstance(dictionary, tuple):
            dictionary = self._collect(dictionary)

        for k, v in dictionary.items():
            setattr(self, k, str(v))

        if not hasattr(self, 'hash'):
            self.hash = self.create_self_hash()

    def header_string(self):
        return self.index + self.timestamp + self.prev_hash + self.data +  self.nonce

    def create_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        return sha.hexdigest()
    
    @staticmethod
    def _collect(block_data):
        info = {}
        info['index'] = block_data[0]
        info['timestamp'] = block_data[1]
        info['prev_hash'] = block_data[2]
        info['hash'] = block_data[3]
        info['data'] = block_data[4]
        info['nonce'] = block_data[5]
        return info

    def __dict__(self):
        info = {}
        info['index'] = self.index
        info['timestamp'] = self.timestamp
        info['prev_hash'] = self.prev_hash
        info['hash'] = self.hash
        info['data'] = self.data
        info['nonce'] = self.nonce
        return info

    def __str__(self):
        return "Block <number: %s, hash: %s>" % (self.index, self.hash)

