"""
Network Setup Script

This script spawns multiple blockchain nodes on different ports.
Each node runs as a separate process.
"""

import subprocess
import time
import signal
import sys
from config import load_config

def spawn_nodes(config):
    """Spawn all node processes"""
    processes = []
    
    for i in range(config["num_nodes"]):
        # Spawn node process
        # In a real implementation, this would start node_framework.py for each node
        # For now, we'll create a simple runner
        print(f"Starting node {i}...")
        # Note: Actual implementation would use multiprocessing or subprocess
        # This is a placeholder - students don't need to modify this
    
    return processes

def main():
    """Main setup function"""
    config = load_config()
    
    print("=" * 50)
    print("Blockchain Network Setup")
    print("=" * 50)
    print(f"Number of nodes: {config['num_nodes']}")
    print(f"Base port: {config['base_port']}")
    print(f"Difficulty: {config['difficulty']} leading zeros")
    print("=" * 50)
    
    # Generate transaction pool if not exists
    import os
    if not os.path.exists("transaction_pool.json"):
        print("Generating transaction pool...")
        from generate_transactions import main as gen_main
        gen_main()
    
    # Spawn nodes
    print("\nStarting nodes...")
    processes = spawn_nodes(config)
    
    print("\nNodes started. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping nodes...")
        for p in processes:
            p.terminate()
        print("All nodes stopped.")

if __name__ == "__main__":
    main()
