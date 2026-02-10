"""
Cryptographic Utilities

This module provides cryptographic functions for hashing, merkle trees,
and digital signatures. Some functions are provided, others students implement.
"""

import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def hash_data(data):
    """
    Hash data using SHA256.
    
    Args:
        data: String or bytes to hash
        
    Returns:
        Hex string (lowercase) of SHA256 hash
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def generate_key_pair():
    """
    Generate a new Ed25519 key pair.
    
    Returns:
        Tuple of (private_key, public_key) objects
    """
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def private_key_to_string(private_key):
    """Convert private key to string for storage"""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

def public_key_to_string(public_key):
    """Convert public key to string for storage"""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

def calculate_merkle_root(transactions):
    """
    Calculate the merkle root of a list of transactions.
    
    This builds a merkle tree from the transactions and returns the root hash.
    The merkle tree allows efficient verification of transaction inclusion.
    
    Algorithm:
    1. Hash each transaction
    2. Pair up hashes and hash them together
    3. Repeat until one hash remains (the root)
    4. If odd number, duplicate last hash
    
    Args:
        transactions: List of Transaction objects or transaction hashes
        
    Returns:
        Merkle root as hex string
    """
    merkleroot = ""
    if not transactions:
        merkleroot = hash_data("")
        return merkleroot

    hashes = []
    for transn in transactions:
        if isinstance(transn,str):
            hashes.append(transn)
        else :
            hashes.append(transn.calculate_hash())

    # now when we have the hashes of all , we need to combine it all the way till root
    while len(hashes) > 1:
        if len(hashes)&1 :
            ##that is the odd case , where we would be needing to duplicate it 
            hashes.append(hashes[-1])

        new_level = []

        ##hash pairwise         
        for i in range(0,len(hashes),2):
            hashes_together = hashes[i]+hashes[i+1]
            new_hash = hash_data(hashes_together)
            new_level.append(new_hash)
        
        hashes = new_level 
        ## with this we would be able to do the whole thing repeatedly , where odd number of hashes at each level could be handled 
    merkleroot = hashes[0]
    return merkleroot

def sign_data(data, private_key):
    """
    Sign data with a private key.
    
    Args:
        data: String or bytes to sign
        private_key: Ed25519 private key object
        
    Returns:
        Signature as bytes
    """
    ## firstly we need to normalize the data to bytes
    if type(data) is str:
        data = data.encode("utf-8")
    ## once we have it in bytes format we may apply the signing algo (ed25519)
    signature = private_key.sign(data)
    return signature

def verify_signature(data, signature, public_key):
    """
    Verify a signature against data and public key.
    
    Args:
        data: Original data that was signed
        signature: Signature bytes
        public_key: Ed25519 public key object
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        return False
    if type(data) is str:
        data = data.encode("utf-8")
    ##signature verification 
    try:
        calc_signature = public_key.verify(signature,data)
        return True 
    except Exception:
        return False

    
