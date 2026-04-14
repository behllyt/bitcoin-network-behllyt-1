import hashlib

def double_sha256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def calculate_merkle_root(txids):
    if len(txids) == 0:
        return None
    
    # Convert txids to bytes in little-endian
    hashes = [bytes.fromhex(txid)[::-1] for txid in txids]
    
    while len(hashes) > 1:
        # If odd number of hashes, duplicate the last one
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        
        new_hashes = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i+1]
            new_hashes.append(double_sha256(combined))
        hashes = new_hashes
    
    # Return in big-endian hex
    return hashes[0][::-1].hex()

# Our block's transaction
txids = [
    "b9a710d730cc305254ff06d32a668056eb5b2dac8671d4873bf39bb1fb5e488e"
]

expected_merkle_root = "b9a710d730cc305254ff06d32a668056eb5b2dac8671d4873bf39bb1fb5e488e"

calculated = calculate_merkle_root(txids)

print("=== Merkle Root Verification ===")
print("Transaction IDs: " + str(txids))
print("Calculated Merkle Root: " + calculated)
print("Expected Merkle Root:   " + expected_merkle_root)
print("Match: " + str(calculated == expected_merkle_root))
