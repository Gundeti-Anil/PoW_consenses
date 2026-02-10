"""
Communication Helper Module

This module provides functions for nodes to communicate and share information.
It handles reading peer log files and getting blockchain state from other nodes.
"""

import json
import os
from config import get_node_log_file, load_config

def get_peer_log_files(node_id, config):
    """
    Get list of log file paths for all peer nodes.
    
    Args:
        node_id: Current node ID (to exclude self)
        config: Configuration dictionary
        
    Returns:
        List of log file paths for peer nodes
    """
    peer_files = []
    for i in range(config["num_nodes"]):
        if i != node_id:
            peer_files.append(get_node_log_file(i))
    return peer_files

def read_node_log(log_file):
    """
    Read blockchain state from a node's log file.
    
    Args:
        log_file: Path to node's log file
        
    Returns:
        Dictionary with node_id and chain, or None if file doesn't exist
    """
    if not os.path.exists(log_file):
        return None
    
    try:
        with open(log_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

def get_all_node_states(node_id, config):
    """
    Get blockchain state from all peer nodes.
    
    Args:
        node_id: Current node ID
        config: Configuration dictionary
        
    Returns:
        Dictionary mapping log_file -> node_state
    """
    peer_files = get_peer_log_files(node_id, config)
    states = {}
    
    for log_file in peer_files:
        state = read_node_log(log_file)
        if state:
            states[log_file] = state
    
    return states

def get_peer_addresses(node_id, config):
    """
    Get list of peer node addresses.
    
    Args:
        node_id: Current node ID
        config: Configuration dictionary
        
    Returns:
        List of peer addresses (localhost:port format)
    """
    base_port = config["base_port"]
    addresses = []
    for i in range(config["num_nodes"]):
        if i != node_id:
            addresses.append(f"localhost:{base_port + i}")
    return addresses
