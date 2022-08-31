from main import all_chain
from app_blockchain.block import Block


def sync():
    nodes = []
    all = all_chain()

    for i in all:
        block = {
            "index": i[0],
            "timestamp": i[1],
            "prev_hash": i[2],
            "hash": i[3],
            "data": i[4],
            "Nonce": i[5]
        }
        nodes.append(Block(block))

    return nodes
