"""
Simple node runner for testing

This script runs a single node for testing purposes.
For full network, use setup_network.py
"""

import sys
from config import load_config
from node_framework import NodeFramework

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_node.py <node_id>")
        print("Example: python run_node.py 0")
        sys.exit(1)
    
    node_id = int(sys.argv[1])
    config = load_config()
    
    if node_id >= config["num_nodes"]:
        print(f"Error: node_id must be < {config['num_nodes']}")
        sys.exit(1)
    
    # Create and start node
    node = NodeFramework(node_id, config)
    
    try:
        node.start()
        
        # Run for a while
        import time
        print(f"Node {node_id} running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            print(f"Node {node_id}: Chain length = {node.get_chain_length()}, PoW = {node.get_cumulative_pow()}")
    
    except KeyboardInterrupt:
        print("\nStopping node...")
        node.stop()

if __name__ == "__main__":
    main()
