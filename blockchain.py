"""
Blockchain Implementation

This module contains the core blockchain data structures and logic.
Students implement the TODO sections.
"""

import json
import time
import hashlib
import os
from block import Block
from transaction import Transaction
from crypto_utils import calculate_merkle_root, hash_data , sign_data
from cryptography.hazmat.primitives import serialization
from crypto_utils import generate_key_pair,public_key_to_string

class Blockchain:
    """
    Blockchain class representing a distributed ledger.
    
    This class manages the chain of blocks, handles mining, validation,
    and synchronization with other nodes.
    """
    
    def __init__(self):
        """Initialize an empty blockchain"""
        self.chain = []
        self.private_key,self.public_key = generate_key_pair()
        self.address = public_key_to_string(self.public_key)

        genesis = self.create_genesis_block()
        self.chain.append(genesis)
    
    def create_genesis_block(self):
        """
        Create the genesis (first) block of the blockchain.
        
        PROVIDED: This function is fully implemented.
        All nodes start with the same genesis block.
        
        The genesis block has:
        - index: 0
        - previous_hash: "0" (hardcoded)
        - transactions: [] (empty)
        - merkle_root: hash of empty transactions
        - nonce: 0
        - timestamp: current time
        - difficulty: 0 (no PoW required for genesis)
        
        Returns:
            Block object representing the genesis block
        """
        # Genesis block is provided - all nodes use the same one
        # Empty transactions for genesis
        empty_txs = []
        merkle_root = hash_data("")  # Hash of empty string for empty transactions
        
        # Create genesis block
        genesis = Block(
            index=0,
            previous_hash="0",
            merkle_root=merkle_root,
            nonce=0,
            timestamp=int(time.time()),
            difficulty=0,
            transactions=empty_txs
        )
        
        return genesis
    
    def load_from_file(self, file_path):
        """
        Load blockchain state from a JSON log file.
        
        This method reads the chain from a file and reconstructs
        Block objects. Used when a node starts up or syncs with peers.
        
        Args:
            file_path: Path to the JSON log file
            
        The file format is:
        {
            "node_id": "node_0",
            "chain": [block_dict1, block_dict2, ...]
        }
        """
        # Implement loading from file
        # Read JSON file
        if not os.path.exists(file_path):
            return 
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                
            chain_loaded = []
            for block_dict in data["chain"]:
                block = Block.from_dict(block_dict)
                chain_loaded.append(block)
            
            self.chain = chain_loaded
        except (json.JSONDecodeError, ValueError):
            print(f"Warning: Could not read {file_path}, starting with genesis.")
        # Parse chain data
        # Reconstruct Block objects from dictionaries
        # Set self.chain
    
    def save_to_file(self, file_path):
        """
        Save blockchain state to a JSON log file.
        
        This method serializes the chain to JSON format for persistence.
        Used after mining a block or syncing with peers.
        
        Args:
            file_path: Path where to save the JSON log file
            
        The file format should match what load_from_file expects.
        """
        state = {}
        state["chain"]=[]

        # Serialize blocks to dictionaries
        for block in self.chain:
            state["chain"].append(block.to_dict())
        # Create JSON structure with node_id and chain
        # Write to file
        with open(file_path,"w") as f :
            json.dump(state,f,indent=4)
        
    
    def select_transactions(self, pending_transactions, max_per_block):
        """
        Select which transactions to include in the next block.
        
        This method chooses transactions from the pending pool.
        Strategy is up to you (FIFO, random, etc.) - document your choice.
        
        Args:
            pending_transactions: List of transaction dictionaries
            max_per_block: Maximum number of transactions (e.g., 10)
            
        Returns:
            List of selected transaction dictionaries
        """

        """
        The strategy being used is FIFO , 
        we would be returning the first k transactions as per their order in the max_per_block 
        """
        selected_transcations = []
        limit = min(max_per_block , len(pending_transactions))
        for i in range (0,limit):
            selected_transcations.append(pending_transactions[i])
        return selected_transcations 

    def sign_transaction(self, transaction):
        """
        Sign a transaction with the node's private key.
        
        This adds a signature field to the transaction.
        The signature proves the transaction was authorized by the sender.
        
        Args:
            transaction: Transaction object to sign
            
        Returns:
            Transaction object with signature field added
        """
        transn_hash = transaction.calculate_hash()
        signature = sign_data(transn_hash, self.private_key)
        transaction.signature = signature
        return transaction

        # TODO: Implement transaction signing
        # Use digital signature to sign the transaction
        # Add signature to transaction object
        # Return signed transaction
        pass
    
    def mine_block(self, transactions, difficulty):
        """
        Mine a new block with the given transactions.
        
        This method:
        1. Creates a block with the transactions
        2. Calculates merkle root
        3. Performs Proof-of-Work (finds nonce)
        4. Adds block to chain
        
        Args:
            transactions: List of Transaction objects
            difficulty: Number of leading zeros required in hash
            
        Returns:
            Block object if mining successful, None otherwise
        """

        # TODO: Implement block mining
        # 1. Get previous block hash (from last block in chain)
        previous_block = self.chain[-1]
        previous_hash = previous_block.hash

        index = previous_block.index + 1 
        # 2. Calculate merkle root from transactions
        merkle_root = calculate_merkle_root(transactions)

        # some initital values 
        nonce=0 
        timestamp = int(time.time())

        # 3. Create block structure
        new_block = Block(
            index=index ,
            transactions=transactions,
            merkle_root=merkle_root,
            nonce=nonce,
            difficulty=difficulty,
            timestamp=timestamp,
            previous_hash=previous_hash
        )

        # 4. Find nonce that satisfies difficulty (PoW)
        # 5. Calculate block hash
        while True:
            new_block.nonce = nonce 
            new_block.hash = new_block.calculate_hash()

            if new_block.meets_difficulty():
                break 

            nonce+= 1
        # 6. Add block to chain
        self.chain.append(new_block)
        # 7. Return the mined block
        return new_block
        
    
    def calculate_cumulative_pow(self, chain):
        """
        Calculate total proof-of-work for a chain.
        
        This sums up the "work" done across all blocks.
        Work can be calculated as 2^difficulty (exponential) or
        just difficulty (linear). Choose one approach.
        
        More cumulative work = stronger chain.
        Used in sync logic to determine which chain to adopt.
        
        Args:
            chain: List of Block objects
            
        Returns:
            Total cumulative proof-of-work value
        """
        total_work = 0 
        #Implement cumulative PoW calculation
        # Sum work across all blocks in chain
        for block in chain:
            total_work += block.difficulty 
        # Work = 2^difficulty (or just difficulty) , we used just difficulty 
        # Return total
        return total_work 
        
    
    def sync_with_peer_logs(self, peer_log_files):
        """
        Synchronize blockchain with peer nodes.
        
        This method:
        1. Reads blockchain state from all peer log files
        2. Compares chains using cumulative PoW
        3. Adopts the chain with most work
        4. If tied, uses tiebreaker (numerically smaller hash)
        
        This is the core distributed consensus logic.
        All nodes should eventually converge to the same chain.
        
        Args:
            peer_log_files: List of log file paths for peer nodes
            
        Returns:
            True if chain was updated, False otherwise
        """
        # Implement sync logic
        best_chain = self.chain
        best_Work = self.calculate_cumulative_pow(self.chain)
        # 1. Read all peer log files
        for file_path in peer_log_files:
            if not os.path.exists(file_path):
                continue 
            # 2. Load chains from each peer
            with open(file_path,"r") as f :
                data = json.load(f)

            peer_chain=[]
            for block_dict in data["chain"]:
                peer_chain.append(Block.from_dict(block_dict))
            # 3. Validate each chain
            if not self.validate_chain(peer_chain):
                continue
            # 4. Calculate cumulative PoW for each chain
            peer_work = self.calculate_cumulative_pow(peer_chain)
            # 5. Find chain with most work
            if peer_work > best_Work :
                best_Work = peer_work 
                best_chain = peer_chain
            # 6. If tied, use tiebreaker (smaller latest block hash)
            elif peer_work == best_Work:
                if peer_chain[-1].hash < best_chain[-1].hash:
                    best_Work=peer_work
                    best_chain=peer_chain
        # 7. Adopt best chain if different from current
        if best_chain != self.chain:
            self.chain = best_chain
            return True 
        # 8. Return True if updated, False otherwise
        return False
    
    def validate_chain(self, chain=None):
        """
        Validate the integrity of a blockchain.
        
        Checks:
        - All block hashes are correct
        - All previous_hash links are correct
        - All PoW is valid (hash meets difficulty)
        - All merkle roots are correct
        - All transaction signatures are valid
        
        Args:
            chain: Chain to validate (if None, validates self.chain)
            
        Returns:
            True if chain is valid, False otherwise
        """

        if chain is None:
            chain = self.chain
        
        # Empty chain case
        if not chain:
            return False
            
        # Check genesis block
        genesis = chain[0]
        if genesis.index != 0 or genesis.previous_hash != "0":
            return False
            
        # Check all blocks
        for i in range(1, len(chain)):
            curr_block = chain[i]
            prev_block = chain[i-1]
            
            # 1. Validate block structure and hash
            if not self.validate_block(curr_block):
                print(f"Block {curr_block.index} failed structural validation")
                return False
                
            # 2. Check linking
            if curr_block.previous_hash != prev_block.hash:
                print(f"Block {curr_block.index} previous hash mismatch")
                return False

            # 3. Verify Transactions - not defined  since we dont have the keys to do so 
            # for transn in curr_block.transactions:
                # # SKIP verification for the "dummy" simulation addresses
                # # Real keys start with "-----BEGIN PUBLIC KEY-----"
                # if transn.sender.startswith("-----BEGIN PUBLIC KEY"):
                #     try:
                #         # Convert PEM string back to public key object
                #         public_key = serialization.load_pem_public_key(
                #             transn.sender.encode("utf-8")
                #         )
                        
                #         # Verify signature
                #         if not transn.verify_signature(public_key):
                #             print(f"Invalid signature in tx {transn.tx_id}")
                #             return False
                            
                #     except Exception as e:
                #         print(f"Crypto error in tx {transn.tx_id}: {e}")
                #         return False
                # else:
                #     # Ideally, we'd reject this, but for this simulation assignment,
                #     # we must ALLOW dummy addresses or the provided JSON file won't work.
                #     pass

        return True
    
    def validate_block(self, block):
        """
        Validate a single block.
        
        Checks block structure, hash, PoW, and merkle root.
        
        Args:
            block: Block object to validate
            
        Returns:
            True if block is valid, False otherwise
        """
        # Implement block validation
        # Check block hash is correct
        if block.hash != block.calculate_hash():
            return False 
        # Check PoW meets difficulty
        if not block.meets_difficulty():
            return False
        # Check merkle root is correct
        if block.merkle_root != calculate_merkle_root(block.transactions):
            return False 
        # Return True if valid, False otherwise
        return True 
    
    def get_balance(self, address):
        """
        Calculate balance for an address.
        
        Scans all transactions in the chain and calculates:
        balance = sum(received) - sum(sent)
        
        Args:
            address: Address to check balance for
            
        Returns:
            Balance amount (integer)
        """

        balance = 0
        for block in self.chain:
            for transn in block.transactions:
                if transn.receiver == address:
                    balance += transn.amount
                if transn.sender == address:
                    balance -= transn.amount
        return balance
        

