# Lab Notes - Bitcoin Network Assignment

## Lab 1: Setting Up a Local Bitcoin Network
Commands executed:
- bitcoin-core.daemon -regtest -daemon
- bitcoin-core.cli -regtest createwallet devwallet
- bitcoin-core.cli -regtest generatetoaddress 101 $ADDRESS
- bitcoin-core.cli -regtest getblockchaininfo

Results:
- Node started successfully in regtest mode
- Wallet devwallet created successfully
- 101 blocks mined to address bcrt1qn80zghuvq9n7p0ua3ddl629xe4awawax4tjf32
- Blockchain height confirmed at 101

Key insight:
- 101 blocks are mined because coinbase rewards only become
  spendable after 100 confirmations

---

## Lab 2: Running Multiple Nodes
Commands executed:
- mkdir -p /home/behlly/snap/bitcoin-core/common/.bitcoin2
- bitcoin-core.daemon -regtest -datadir=.../.bitcoin2 -port=18445 -rpcport=18446 -daemon
- bitcoin-core.cli -regtest addnode 127.0.0.1:18445 onetry

Results:
- Second node started successfully on port 18445
- RPC communication between nodes limited by snap installation

Error encountered:
- Snap version restricts multi-node RPC on same machine
- Documented limitation, second node started but RPC unreachable

Key insight:
- In production, nodes connect over TCP on port 8333
- Each node maintains its own copy of the blockchain

---

## Lab 3: Transaction Propagation and Mempool
Commands executed:
- bitcoin-core.cli -regtest sendtoaddress $RECV_ADDR 5.0
- bitcoin-core.cli -regtest getmempoolinfo
- bitcoin-core.cli -regtest getrawmempool
- bitcoin-core.cli -regtest generatetoaddress 1 $ADDRESS
- bitcoin-core.cli -regtest gettransaction $TXID

Results:
- Transaction sent successfully
- TXID: c5d101b3f4b7c12b1da597b1639c7a63623c8e9a7f938c3c0329271669a26c0a
- Transaction appeared in mempool immediately
- After mining 1 block, transaction confirmed with 1 confirmation

Error encountered:
- Fee estimation failed initially, fixed by restarting with -fallbackfee=0.0001

Key insight:
- Mempool is a waiting room for unconfirmed transactions
- Miners pick transactions from mempool to include in blocks

---

## Lab 4: Compact Block Relay (BIP152)
Commands executed:
- tail ~/snap/bitcoin-core/common/.bitcoin/regtest/debug.log | grep -i compact
- bitcoin-core.cli -regtest generatetoaddress 1 $ADDRESS

Results:
- Compact blocks enabled by default in Bitcoin Core v30.2.0
- No compact block messages visible in single node regtest mode

Key insight:
- BIP152 reduces bandwidth by sending block sketches instead of full blocks
- Peers only request missing transactions they dont already have
- Requires multiple connected peers to observe negotiation

---

## Lab 5: Compact Block Filters (BIP157/158)
Commands executed:
- bitcoin-core.daemon -regtest -fallbackfee=0.0001 -blockfilterindex=1 -daemon
- bitcoin-core.cli -regtest getblockfilter $BLOCK_HASH

Results:
- Filter: 011d9b30
- Header: c913588eeb9fa542242e632e28d5799fbce65b0ed286a16da8f064e9ea15f353

Key insight:
- Block filters allow lightweight clients to check if a block
  contains their transactions without downloading the full block
- Uses Golomb-Rice encoding for compact representation

---

## Lab 6: Merkle Tree Exploration
Commands executed:
- bitcoin-core.cli -regtest getbestblockhash
- bitcoin-core.cli -regtest getblock $BLOCK_HASH
- python3 code/merkle_verification.py

Results:
- Merkle root: b9a710d730cc305254ff06d32a668056eb5b2dac8671d4873bf39bb1fb5e488e
- Calculated merkle root matched expected merkle root
- Match: True

Key insight:
- With only 1 transaction, merkle root equals the txid itself
- Merkle trees allow efficient proof that a transaction is in a block

---

## Lab 7: Bloom Filters (BIP37)
Commands executed:
- python3 code/bloom_filter_demo.py

Results:
- Bloom filter created with capacity 1000 and error rate 0.001
- Known txids correctly identified as present
- Unknown txids correctly identified as absent

Key insight:
- Bloom filters are probabilistic - false positives possible
- BIP37 deprecated due to privacy leaks
- Replaced by BIP157/158 compact block filters

---

## Lab 8: Observing Consensus Rules
Results:
- All transactions validated before mempool acceptance
- Invalid transactions rejected immediately
- Consensus rules enforced at every node independently

Key insight:
- Consensus rules are the backbone of Bitcoin security
- Every node validates independently - no central authority needed

---

## Lab 9: Visualizing Peer Connections
Commands executed:
- bitcoin-core.cli -regtest getnetworkinfo
- bitcoin-core.cli -regtest getpeerinfo

Results:
- Network info retrieved successfully
- No peers in single node regtest mode

Key insight:
- Each peer connection is a TCP link
- Nodes exchange messages like inv, getdata, block, tx
