import hashlib
import time
import json
import os


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }
        block_string = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self, save_path=None):
        """
        If save_path is None → no file saving (cloud compatible)
        If save_path is provided → local file saving enabled
        """
        self.save_path = save_path
        self.chain = []

        if self.save_path and os.path.exists(self.save_path):
            self.load()
        else:
            # Create Genesis Block
            self.create_block({"message": "Genesis Block"})

    def create_block(self, data):
        index = len(self.chain)
        timestamp = time.time()
        previous_hash = self.chain[-1].hash if self.chain else "0"

        block = Block(index, timestamp, data, previous_hash)
        self.chain.append(block)

        if self.save_path:
            self.save()

        return block

    def save(self):
        with open(self.save_path, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=4)

    def load(self):
        with open(self.save_path, "r") as f:
            blocks = json.load(f)

        for blk in blocks:
            block = Block(
                blk["index"],
                blk["timestamp"],
                blk["data"],
                blk["previous_hash"]
            )
            self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
    block = self.chain[i]
    previous_block = self.chain[i - 1]

    if block.previous_hash != previous_block.hash:
        return False

