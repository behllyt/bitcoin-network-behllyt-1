# assignment-5
# Bitcoin Network


## Overview

This assignment consists of hands-on labs exploring Bitcoin's network architecture, transaction propagation, and block validation mechanisms. You'll work with Bitcoin Core in regtest mode to safely experiment with blockchain operations.


## Hands-On Bitcoin Network Labs

Complete the following labs using Bitcoin Core in regtest mode.

---

### Lab 1: Setting Up a Local Bitcoin Network

**Step 1: Initialize Regtest Environment**

```bash
bitcoind -regtest -daemon
```

Launches a local Bitcoin node in regression test mode.

**Step 2: Create a Wallet**

```bash
bitcoin-cli -regtest createwallet devwallet
```

Creates a wallet named `devwallet` for testing.

**Step 3: Generate Some Coins**

```bash
ADDRESS=$(bitcoin-cli -regtest getnewaddress)
bitcoin-cli -regtest generatetoaddress 101 $ADDRESS
```

Mines 101 blocks to your address — gives you spendable test BTC.

**Expected output:** Block hashes printed in terminal.

**Step 4: Verify Blockchain Info**

```bash
bitcoin-cli -regtest getblockchaininfo
```

Confirms height, difficulty, and network details.

---

### Lab 2: Running Multiple Nodes (Simulated Network)

Simulate transaction propagation by running multiple nodes on different ports.

**Step 1: Start Second Node**

```bash
mkdir -p ~/bitcoin-node2
bitcoind -regtest -datadir=~/bitcoin-node2 -port=18445 -rpcport=18446 -daemon
```

**Step 2: Connect Nodes**

```bash
bitcoin-cli -regtest addnode 127.0.0.1:18445 onetry
```

**Step 3: Verify Connection**

```bash
bitcoin-cli -regtest getpeerinfo | jq '.[].addr'
```

You should see `127.0.0.1:18445` listed.

---

### Lab 3: Transaction Propagation and the Mempool

**Step 1: Send a Transaction**

```bash
RECV_ADDR=$(bitcoin-cli -regtest getnewaddress)
bitcoin-cli -regtest sendtoaddress $RECV_ADDR 5.0
```

**Step 2: Check Mempool**

```bash
bitcoin-cli -regtest getmempoolinfo
bitcoin-cli -regtest getrawmempool | jq '.'
```

Displays current transactions waiting to be mined.

**Step 3: Mine the Transaction**

```bash
bitcoin-cli -regtest generatetoaddress 1 $ADDRESS
```

Confirms the transaction in a new block.

**Step 4: Verify Confirmation**

```bash
TXID=<your_txid>
bitcoin-cli -regtest gettransaction $TXID
```

**Expected:** `confirmations: 1`

---

### Lab 4: Compact Block Relay (BIP152)

**Objective:** Observe reduced bandwidth during block propagation.

**Note:** For demonstration, run `bitcoind` with `-printtoconsole` and enable `-debug=net`.

**Step 1: Enable Compact Blocks**

Compact blocks are automatically supported in Bitcoin Core since 0.13.0. To view negotiation:

```bash
tail -f ~/.bitcoin/regtest/debug.log | grep compact
```

You'll see messages like `sendcmpct` and `cmpctblock`.

**Step 2: Mine a Block and Observe**

```bash
bitcoin-cli -regtest generatetoaddress 1 $ADDRESS
```

Watch for compact block announcements in debug logs.

---

### Lab 5: Compact Block Filters (BIP157/158)

**Step 1: Run a Node with Compact Filter Index**

```bash
bitcoind -regtest -daemon -blockfilterindex=1
```

**Step 2: Query Block Filter**

```bash
BLOCK_HASH=$(bitcoin-cli -regtest getblockhash 1)
bitcoin-cli -regtest getblockfilter $BLOCK_HASH
```

Returns filter header and filter data (Golomb-Rice encoded bitstream).

**Step 3: Decode Filter (Optional)**

Install neutrino or btcd client to test SPV-like behavior locally.

---

### Lab 6: Merkle Tree Exploration

**Step 1: Get Block Hash**

```bash
BLOCK_HASH=$(bitcoin-cli -regtest getbestblockhash)
```

**Step 2: Inspect Block Details**

```bash
bitcoin-cli -regtest getblock $BLOCK_HASH true
```

Note the `merkleroot` field.

**Step 3: Verify Merkle Root Manually (Python example)**

```python
import hashlib

def double_sha256(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()

txids = [bytes.fromhex(txid)[::-1] for txid in ["<txid1>", "<txid2>"]]
root = double_sha256(txids[0] + txids[1])[::-1].hex()
print(root)
```

Matches the block's `merkleroot`.

---

### Lab 7: Bloom Filters (BIP37)

**Step 1: Use bitcoin-cli RPC (legacy)**

```bash
bitcoin-cli -regtest setnetworkactive false
```

Add peers manually with support for BIP37 (use bitcoinj or older btcd client).

**Step 2: Generate a Bloom Filter**

```python
from pybloom_live import BloomFilter

bf = BloomFilter(capacity=1000, error_rate=0.001)
bf.add('my_txid')
print(bf.bitarray)
```

Demonstrate how probabilistic matching works.

**Discussion:** Emphasize deprecation due to privacy leaks (clients revealed interests).

---

### Lab 8: Observing Consensus Rules

**Step 1: Corrupt a Block (for demo only)**

```bash
cp ~/.bitcoin/regtest/blocks/blk00000.dat ~/tmp/
# Manually edit a byte — breaks validation
```

**Step 2: Restart Node**

```bash
bitcoind -regtest -daemon
```

Node rejects the corrupted block → `error: bad-blk` in logs.

**Lesson:** Consensus rules are strict; invalid data is rejected network-wide.

---

### Lab 9: Visualizing Peer Connections

**Step 1: View Network Graph**

```bash
bitcoin-cli -regtest getpeerinfo | jq '[.[] | {addr, subver, inbound}]'
```

**Step 2: Use bitcoin-cli getnetworkinfo**

```bash
bitcoin-cli -regtest getnetworkinfo
```

Displays peer count, local services, relay fees, and protocol version.

**Tip:** Each peer connection is a TCP link exchanging compact messages — similar to sockets in general networking.

---

### Lab 10: Cleanup

**Stop all nodes:**

```bash
bitcoin-cli -regtest stop
bitcoin-cli -datadir=~/bitcoin-node2 -regtest stop
```

**Remove temporary files (optional):**

```bash
rm -rf ~/bitcoin-node2 ~/.bitcoin/regtest
```

---

## Submission Guidelines

### What to Submit

Your submission should include:

```
📁 assignment-5-submission/
├── README.md (your main report)
├── lab-screenshots or output.txt file/ 
│   ├── lab1-setup.png/lab1.txt
│   ├── lab3-mempool.png
│   ├── lab6-merkle.png
│   └── ...
├── code/ (any scripts you created)
│   ├── merkle_verification.py
│   └── bloom_filter_demo.py
└── lab-notes.md (observations and findings from each lab)
```

### Documentation Requirements

For each lab, document:
- Commands you executed
- Output/results observed
- Any errors encountered and how you resolved them
- Key insights or learnings

---

## Learning Objectives

By completing this assignment, you will:

- Experience transaction propagation and mempool behavior
- Observe how BIPs (152, 157, 158) optimize bandwidth and privacy
- Understand how consensus ensures integrity and immutability
- Gain hands-on experience with Bitcoin Core RPC commands

---

## Resources

### Blockchain Explorers
- [Mempool.space](https://mempool.space) - Clean UI, detailed information
- [Blockchain.com](https://www.blockchain.com/explorer) - Classic explorer
- [Blockstream.info](https://blockstream.info) - Technical details

### Documentation
- [Bitcoin Core RPC Documentation](https://developer.bitcoin.org/reference/rpc/)
- [Bitcoin Developer Guide](https://developer.bitcoin.org/devguide/)
- [BIP152 - Compact Block Relay](https://github.com/bitcoin/bips/blob/master/bip-0152.mediawiki)
- [BIP157/158 - Compact Block Filters](https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki)

### Tools
- [Bitcoin Core](https://bitcoincore.org/en/download/)
- [jq - JSON processor](https://stedolan.github.io/jq/)
- [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)

---

## Tips

- Start with Lab 1 to ensure your environment is properly set up
- Take screenshots at each step for your submission
- Keep notes as you work through the labs
- If you encounter errors, check the debug logs: `~/.bitcoin/regtest/debug.log`
- Don't forget to stop your nodes when finished to free up resources

---

## Troubleshooting

**Node won't start:**
- Check if another instance is already running
- Verify you have enough disk space
- Check permissions on the Bitcoin data directory

**Can't connect to RPC:**
- Ensure the node is running (`ps aux | grep bitcoind`)
- Verify you're using the correct port and datadir parameters

**Transaction not appearing in mempool:**
- Ensure you have sufficient funds
- Check the transaction fee is adequate
- Verify the receiving address is valid

---

## Questions?

If you have questions about the assignment:
- Open an issue in this repository
- Ask during office hours

---

## Conclusion

By completing these labs, you'll gain practical understanding of:
- How Bitcoin nodes communicate and propagate data
- How mempool, blocks, and filters interact
- How consensus ensures network integrity
- Real-world Bitcoin Core operations

**Next step:** Integrate these insights into Bitcoin Core RPC automation or monitoring scripts to extend your infrastructure-level understanding.

Good luck! 🚀
