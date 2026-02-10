import subprocess
import time
import requests
import json
from multiprocessing import Process

# Configuration
NUM_NODES = 5
BASE_PORT = 5000
NODE_SCRIPT = "run_node.py"

def start_node(node_id):
    """Start a single node in a subprocess."""
    port = BASE_PORT + node_id
    print(f"Starting node {node_id} on port {port}")
    return subprocess.Popen(["python", NODE_SCRIPT, str(node_id)])

def verify_node(node_id):
    """Verify that a node is running and return its status."""
    port = BASE_PORT + node_id
    try:
        response = requests.get(f"http://localhost:{port}/status", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def monitor_nodes():
    """Monitor all nodes and display their status."""
    print("\n=== Node Status ===")
    for i in range(NUM_NODES):
        status = verify_node(i)
        if status:
            print(f"Node {i}: Running (Chain length: {status.get('chain_length', 'N/A')}, "
                  f"Peers: {len(status.get('peers', []))})")
        else:
            print(f"Node {i}: Not responding")

def main():
    # Start all nodes
    processes = []
    for i in range(NUM_NODES):
        p = Process(target=start_node, args=(i,))
        p.start()
        processes.append(p)
        time.sleep(1)  # Give each node a moment to start

    try:
        # Initial status
        time.sleep(5)  # Wait for nodes to initialize
        monitor_nodes()
        
        # Keep monitoring until interrupted
        while True:
            time.sleep(10)
            monitor_nodes()
            
    except KeyboardInterrupt:
        print("\nShutting down nodes...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()

if __name__ == "__main__":
    main()