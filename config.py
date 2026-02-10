"""
Configuration loader for blockchain assignment
"""

import json

def load_config(config_file="config.json"):
    """Load configuration from JSON file"""
    with open(config_file, "r") as f:
        return json.load(f)

def get_node_addresses(config):
    """Get list of all node addresses"""
    addresses = []
    base_port = config["base_port"]
    for i in range(config["num_nodes"]):
        addresses.append(f"localhost:{base_port + i}")
    return addresses

def get_node_log_file(node_id):
    """Get log file path for a node"""
    return f"node_{node_id}_blockchain.json"
