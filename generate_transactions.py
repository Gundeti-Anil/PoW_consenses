"""
Transaction Pool Generator

This script generates a transaction pool with multiple permutations.
Each permutation contains all transactions in a different order.
Nodes are assigned permutations based on config parameters.
"""

import json
import random
import hashlib
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config

def generate_addresses(num_addresses):
    """Generate random addresses for transactions"""
    addresses = []
    for i in range(num_addresses):
        # Simple address generation (can be improved)
        addr = hashlib.sha256(f"address_{i}".encode()).hexdigest()[:16]
        addresses.append(addr)
    return addresses

def generate_transactions(num_transactions, addresses, initial_balance):
    """Generate valid transactions"""
    transactions = []
    random.seed(42)  # For reproducibility
    
    for i in range(num_transactions):
        sender = random.choice(addresses)
        receiver = random.choice([a for a in addresses if a != sender])
        amount = random.randint(1, 100)
        
        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "tx_id": f"tx_{i:03d}"
        }
        transactions.append(tx)
    
    return transactions

def create_permutations(transactions, num_permutations):
    """Create different orderings of transactions"""
    permutations = []
    random.seed(42)  # For reproducibility
    
    for i in range(num_permutations):
        perm = transactions.copy()
        random.shuffle(perm)
        permutations.append(perm)
    
    return permutations

def assign_permutations_to_nodes(permutations, num_nodes):
    """Assign permutations to nodes"""
    num_permutations = len(permutations)
    nodes_per_permutation = (num_nodes + num_permutations - 1) // num_permutations  # Ceil division
    
    assignment = {}
    perm_idx = 0
    
    for node_id in range(num_nodes):
        if node_id % nodes_per_permutation == 0 and node_id > 0:
            perm_idx = (perm_idx + 1) % num_permutations
        
        assignment[f"node_{node_id}"] = {
            "permutation_id": perm_idx,
            "transactions": permutations[perm_idx]
        }
    
    return assignment

def main():
    config = load_config()
    
    # Generate addresses (more than needed for variety)
    num_addresses = 20
    addresses = generate_addresses(num_addresses)
    
    # Generate transactions
    transactions = generate_transactions(
        config["transaction_pool_size"],
        addresses,
        config["initial_balance"]
    )
    
    # Create permutations
    permutations = create_permutations(transactions, config["num_permutations"])
    
    # Assign to nodes
    node_assignments = assign_permutations_to_nodes(permutations, config["num_nodes"])
    
    # Save transaction pool
    pool_data = {
        "all_transactions": transactions,
        "permutations": permutations,
        "node_assignments": node_assignments,
        "addresses": addresses,
        "initial_balances": {addr: config["initial_balance"] for addr in addresses}
    }
    
    with open("transaction_pool.json", "w") as f:
        json.dump(pool_data, f, indent=2)
    
    print(f"Generated {len(transactions)} transactions")
    print(f"Created {len(permutations)} permutations")
    print(f"Assigned to {config['num_nodes']} nodes")
    print("Transaction pool saved to transaction_pool.json")

if __name__ == "__main__":
    main()
