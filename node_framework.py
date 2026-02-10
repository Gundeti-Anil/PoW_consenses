"""
Node Framework

This module provides the framework for running blockchain nodes.
It handles node lifecycle, mining triggers, and sync coordination.
Students' Blockchain class is integrated here.
"""

import json
import os
import time
import threading
from config import load_config, get_node_log_file, get_node_addresses
from comm import get_peer_log_files, get_all_node_states
from transaction import Transaction
from blockchain import Blockchain

class NodeFramework:
    """
    Framework for running a blockchain node.
    This handles orchestration - students implement Blockchain class logic.
    """
    
    def __init__(self, node_id, config):
        self.node_id = node_id
        self.config = config
        self.log_file = get_node_log_file(node_id)
        self.blockchain = Blockchain()
        self.running = False
        self.mining_thread = None
        self.sync_thread = None
        
        # CRITICAL FIX: Add lock to prevent mining during sync
        self.chain_lock = threading.Lock()
        
        # Load initial state
        self._load_blockchain()
        
        # Load transaction assignments
        self._load_transaction_assignments()
    
    def _load_blockchain(self):
        """Load blockchain from log file or create genesis"""
        if os.path.exists(self.log_file):
            self.blockchain.load_from_file(self.log_file)
        else:
            # Create genesis block
            genesis = self.blockchain.create_genesis_block()
            self.blockchain.chain = [genesis]
            self._save_blockchain()
    
    def _save_blockchain(self):
        """Save blockchain to log file"""
        # CRITICAL FIX: Use lock when saving
        with self.chain_lock:
            self.blockchain.save_to_file(self.log_file)
    
    def _load_transaction_assignments(self):
        """Load assigned transactions from transaction pool"""
        with open("transaction_pool.json", "r") as f:
            pool_data = json.load(f)
        
        node_key = f"node_{self.node_id}"
        if node_key in pool_data["node_assignments"]:
            self.assigned_transactions = pool_data["node_assignments"][node_key]["transactions"]
        else:
            self.assigned_transactions = []
    
    def _mining_loop(self):
        """Continuous mining loop"""
        while self.running:
            try:
                # CRITICAL FIX: Acquire lock before mining
                with self.chain_lock:
                    # Get pending transactions (from assigned set)
                    pending = [tx for tx in self.assigned_transactions if not self._is_transaction_mined(tx)]
                    
                    if len(pending) > 0:
                        # Select transactions to mine (students implement selection logic)
                        selected = self.blockchain.select_transactions(
                            pending,
                            self.config["max_transactions_per_block"]
                        )
                        
                        if len(selected) > 0:
                            # Sign transactions (students implement)
                            signed_txs = []
                            for tx_dict in selected:
                                tx = Transaction.from_dict(tx_dict)
                                # Students implement signing
                                signed_tx = self.blockchain.sign_transaction(tx)
                                signed_txs.append(signed_tx)
                            
                            # Mine block (students implement)
                            block = self.blockchain.mine_block(
                                signed_txs,
                                self.config["difficulty"]
                            )
                            
                            if block:
                                # Save inside the lock
                                self.blockchain.save_to_file(self.log_file)
                                # Note: sync will happen in sync_loop
                
                # CRITICAL FIX: Add delay after releasing lock
                # This gives sync thread a chance to run
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Node {self.node_id} mining error: {e}")
                time.sleep(1)
    
    def _is_transaction_mined(self, tx_dict):
        """Check if transaction is already in blockchain"""
        tx_id = tx_dict.get("tx_id")
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if isinstance(tx, dict) and tx.get("tx_id") == tx_id:
                    return True
                elif hasattr(tx, "tx_id") and tx.tx_id == tx_id:
                    return True
        return False
    
    def _sync_loop(self):
        """Periodic sync loop"""
        while self.running:
            time.sleep(self.config["sync_frequency_seconds"])
            self._trigger_sync()
    
    def _trigger_sync(self):
        """Trigger sync with peers"""
        try:
            # CRITICAL FIX: Acquire lock during sync
            with self.chain_lock:
                peer_files = get_peer_log_files(self.node_id, self.config)
                updated = self.blockchain.sync_with_peer_logs(peer_files)
                if updated:
                    # Save inside the lock
                    self.blockchain.save_to_file(self.log_file)
        except Exception as e:
            print(f"Node {self.node_id} sync error: {e}")
    
    def start(self):
        """Start the node (mining and syncing)"""
        self.running = True
        
        # Initial sync
        self._trigger_sync()
        
        # Start mining thread
        self.mining_thread = threading.Thread(target=self._mining_loop, daemon=True)
        self.mining_thread.start()
        
        # Start sync thread
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        
        print(f"Node {self.node_id} started")
    
    def stop(self):
        """Stop the node"""
        self.running = False
        if self.mining_thread:
            self.mining_thread.join(timeout=1)
        if self.sync_thread:
            self.sync_thread.join(timeout=1)
        print(f"Node {self.node_id} stopped")
    
    def get_chain_length(self):
        """Get current chain length"""
        with self.chain_lock:
            return len(self.blockchain.chain)
    
    def get_cumulative_pow(self):
        """Get cumulative PoW of current chain"""
        with self.chain_lock:
            return self.blockchain.calculate_cumulative_pow(self.blockchain.chain)