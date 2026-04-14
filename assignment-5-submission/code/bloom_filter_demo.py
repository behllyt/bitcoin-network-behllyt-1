from pybloom_live import BloomFilter

def demo_bloom_filter():
    print("=== Bloom Filter Demo ===")
    print("")
    
    # Create a bloom filter
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    
    # Add some transaction IDs
    txids = [
        "c5d101b3f4b7c12b1da597b1639c7a63623c8e9a7f938c3c0329271669a26c0a",
        "b9a710d730cc305254ff06d32a668056eb5b2dac8671d4873bf39bb1fb5e488e",
        "my_address_1",
        "my_address_2"
    ]
    
    print("Adding items to bloom filter...")
    for txid in txids:
        bf.add(txid)
        print("Added: " + txid)
    
    print("")
    print("=== Testing Membership ===")
    
    # Test items that are in the filter
    test_items = [
        "c5d101b3f4b7c12b1da597b1639c7a63623c8e9a7f938c3c0329271669a26c0a",
        "b9a710d730cc305254ff06d32a668056eb5b2dac8671d4873bf39bb1fb5e488e",
        "unknown_txid_not_added",
        "another_unknown_txid"
    ]
    
    for item in test_items:
        result = item in bf
        print("Item: " + item[:20] + "... -> In filter: " + str(result))
    
    print("")
    print("=== Bloom Filter Stats ===")
    print("Capacity: 1000")
    print("Error rate: 0.001 (0.1%)")
    print("Items added: " + str(len(txids)))
    print("")
    print("=== How Bitcoin Uses Bloom Filters (BIP37) ===")
    print("1. SPV client creates a bloom filter with its addresses")
    print("2. Client sends filter to full node")
    print("3. Full node checks transactions against filter")
    print("4. Only matching transactions are sent to client")
    print("5. This saves bandwidth for lightweight clients")
    print("Note: BIP37 is deprecated due to privacy leaks")

if __name__ == "__main__":
    demo_bloom_filter()
