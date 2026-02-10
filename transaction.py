"""
Transaction Data Structure

This module defines the Transaction class representing a single transaction.
Students implement the TODO sections.
"""

import json
from crypto_utils import hash_data,verify_signature

class Transaction:
    """
    Transaction class representing a transfer of value.
    
    A transaction contains:
    - sender: Address of sender
    - receiver: Address of receiver
    - amount: Amount to transfer
    - tx_id: Unique transaction identifier
    - signature: Digital signature (added when signed)
    """
    
    def __init__(self, sender, receiver, amount, tx_id, signature=None):
        """
        Initialize a transaction.
        
        Args:
            sender: Sender address
            receiver: Receiver address
            amount: Transfer amount
            tx_id: Unique transaction ID
            signature: Digital signature (None if not signed)
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.tx_id = tx_id
        self.signature = signature
    
    def calculate_hash(self):
        """
        Calculate hash of transaction data.
        
        Hash should include: sender, receiver, amount, tx_id.
        Signature is NOT included in hash (it signs the hash).
        
        Returns:
            Transaction hash as hex string
        """
        total_val = f"{self.sender}|{self.receiver}|{self.amount}|{self.tx_id}"
        hashed_value = hash_data(total_val)
        return hashed_value
        
    
    def to_dict(self):
        """
        Serialize transaction to dictionary.
        
        Returns:
            Dictionary representation of transaction
        """
        sig_str = None
        if self.signature:
            #if its already a string keep it , ow hex it 
            if isinstance(self.signature, bytes):
                sig_str = self.signature.hex()
            else :
                sig_str = self.signature
        
        dictionary = {"sender":self.sender,
                      "receiver":self.receiver,
                      "amount":self.amount,
                      "tx_id":self.tx_id,
                      "signature":sig_str}
        return dictionary
    
    @classmethod
    def from_dict(cls, tx_dict):
        """
        Deserialize transaction from dictionary.
        
        Args:
            tx_dict: Dictionary representation of transaction
            
        Returns:
            Transaction object
        """
        # Convert hex string back to bytes if it exists
        signature = tx_dict.get("signature")
        if signature and isinstance(signature, str):
            try:
                signature = bytes.fromhex(signature)
            except ValueError:
                pass
                
        return cls(
            sender=tx_dict["sender"],
            receiver=tx_dict["receiver"],
            amount=tx_dict["amount"],
            tx_id=tx_dict["tx_id"],
            signature=signature
        )
    
    def verify_signature(self, public_key):
        """
        Verify the digital signature of this transaction.
        
        Uses the public key to verify that the signature is valid
        for this transaction's data.
        
        Args:
            public_key: Public key to verify signature against
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.signature:
            return False
        
        transn_hash = self.calculate_hash()

        return verify_signature(transn_hash,self.signature,public_key)
        
