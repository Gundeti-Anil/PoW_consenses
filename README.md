# Blockchain Implementation

This is a Python implementation of a Proof-of-Work (PoW) based blockchain with a peer-to-peer network. The project includes core blockchain functionality, transaction handling, and node networking capabilities.

## Project Structure

- [blockchain.py] Core blockchain implementation with mining and validation logic
- [block.py]: Block data structure and validation
- [transaction.py]: Transaction data structure and validation
- [crypto_utils.py]: Cryptographic utilities (hashing, signatures, Merkle trees)
- [node_framework.py]: Node management and orchestration
- [network.py]: Network communication between nodes
- [run_node.py]: Script to start a blockchain node
- [setup_network.py]: Script to set up the test network
- [generate_transactions.py]: Utility to generate test transactions
- [config.py] & [config.json]: Configuration management
- [comm.py]: Communication utilities

## Key Features

1. **Blockchain Core**
   - Proof-of-Work consensus
   - Block validation
   - Transaction validation
   - Merkle tree implementation
   - Digital signatures for transactions

2. **Networking**
   - Peer-to-peer node communication
   - Blockchain synchronization
   - Transaction propagation
   - Node discovery

3. **Node Management**
   - Multiple node support
   - Persistent storage
   - Logging
   - Configuration management

## Getting Started

### Prerequisites

- Python 3.6+
- Required packages (install via `pip install -r requirements.txt`)

### Running the Network

1. **Set up the network**:
   ```bash
   python setup_network.py

2. **Start nodes**:
   ```bash
   python network.py

