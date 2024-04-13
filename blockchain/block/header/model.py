import datetime as date


class Header:
    def __init__(self, index, timestamp, prev_hash, nonce):
        self.index = index
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.nonce = nonce

    def get_data_string(self):
        string_data = [self.index, self.timestamp, self.prev_hash, self.nonce]
        return ''.join(map(str, string_data))

    @classmethod
    def create_now(cls, index, prev_hash, nonce):
        timestamp = date.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return cls(index, timestamp, prev_hash, nonce)
