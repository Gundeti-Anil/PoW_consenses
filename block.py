"""
Block Data Structure

This module defines the Block class representing a single block in the blockchain.
Students implement the TODO sections.
"""

import time
import hashlib
from crypto_utils import hash_data
from transaction import Transaction

class Block:
    """
    Block class representing a single block in the blockchain.
    
    A block contains:
    - Header: index, previous_hash, merkle_root, nonce, timestamp, difficulty
    - Body: list of transactions
    - Hash: cryptographic hash of the entire block
    """
    
    def __init__(self, index, previous_hash, merkle_root, nonce, timestamp, difficulty, transactions, hash_value=None):
        """
        Initialize a block.
        
        Args:
            index: Block number (0 for genesis, 1, 2, ...)
            previous_hash: Hash of previous block
            merkle_root: Root of transaction merkle tree
            nonce: Proof-of-Work nonce value
            timestamp: Unix timestamp
            difficulty: PoW difficulty level
            transactions: List of Transaction objects
            hash_value: Pre-calculated hash (if None, will be calculated)
        """
        self.index = index
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.transactions = transactions
        self.hash = hash_value or self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate the cryptographic hash of this block.
        
        The hash should be computed over all block data:
        - Header fields (index, previous_hash, merkle_root, nonce, timestamp, difficulty)
        - Transactions (or their hashes)
        
        Uses SHA256 and returns hex string (lowercase).
        
        Returns:
            Block hash as hex string
        """
        total_data =f"{self.index}|{self.previous_hash}|{self.merkle_root}|{self.nonce}|{self.timestamp}|{self.difficulty}"
        
        return hash_data(total_data)
    
    
    def to_dict(self):
        """
        Serialize block to dictionary for JSON storage.
        
        Converts block to a format that can be saved to log files.
        Transactions should also be serialized.
        
        Returns:
            Dictionary representation of block
        """
        dictionary = {
            "index":self.index ,
            "previous_hash":self.previous_hash,
            "merkle_root":self.merkle_root,
            "nonce":self.nonce,
            "timestamp":self.timestamp,
            "difficulty":self.difficulty,
            "transactions":[tx.to_dict() for tx in self.transactions],
            "hash":self.hash
        }
        return dictionary 
    
    @classmethod
    def from_dict(cls, block_dict):
        """
        Deserialize block from dictionary.
        
        Reconstructs Block object from JSON/log file data.
        Transactions should also be deserialized.
        
        Args:
            block_dict: Dictionary representation of block
            
        Returns:
            Block object
        """
        transactions = [
            Transaction.from_dict(tx)
            for tx in block_dict["transactions"]
        ]
        return cls(
            index = block_dict["index"],
            previous_hash = block_dict["previous_hash"],
            merkle_root = block_dict["merkle_root"],
            nonce = block_dict["nonce"],
            timestamp = block_dict["timestamp"],
            difficulty = block_dict["difficulty"],
            transactions = transactions ,
            hash_value = block_dict["hash"]
        )

        # TODO: Implement deserialization
        # Parse dictionary
        # Reconstruct Block object
        # Deserialize transactions
        # Return Block
    
    
    def meets_difficulty(self):
        """
        Check if block hash meets the difficulty requirement.
        
        Difficulty means the hash must start with N leading zeros,
        where N is the difficulty value.
        
        Returns:
            True if hash meets difficulty, False otherwise
        """
        diff_level = self.difficulty 
        hash_val = self.hash 
        for i in range (0,diff_level):
            if hash_val[i] != '0':
                return False
        
        return True

        # TODO: Implement difficulty check
        # Check if hash starts with required number of zeros
        # Return True/False

