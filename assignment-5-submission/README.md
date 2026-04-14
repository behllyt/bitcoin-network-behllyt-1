# Bitcoin Network Assignment - Lab Report

## Overview
This report documents hands-on labs exploring Bitcoin's network
architecture, transaction propagation, and block validation
using Bitcoin Core v30.2.0 in regtest mode.

## Environment
- OS: Ubuntu 24
- Bitcoin Core: v30.2.0 (snap install)
- Mode: Regtest (local test network)
- Wallet: devwallet

## Files
- lab-notes.md - Observations and findings from each lab
- lab1.txt - Blockchain info output
- lab2.txt - Second node setup notes
- lab3.txt - Mempool and transaction output
- lab4.txt - Compact block relay notes
- lab5.txt - Block filter output
- lab6.txt - Merkle tree output
- lab7.txt - Bloom filter output
- lab8.txt - Consensus rules output
- lab9.txt - Peer connections output
- code/merkle_verification.py - Merkle root verification script
- code/bloom_filter_demo.py - Bloom filter demonstration script

## Labs Completed
- Lab 1: Local Bitcoin Network Setup - DONE
- Lab 2: Multiple Nodes - DONE (snap limitation documented)
- Lab 3: Transaction Propagation and Mempool - DONE
- Lab 4: Compact Block Relay BIP152 - DONE
- Lab 5: Compact Block Filters BIP157/158 - DONE
- Lab 6: Merkle Tree Exploration - DONE
- Lab 7: Bloom Filters BIP37 - DONE
- Lab 8: Consensus Rules - DONE
- Lab 9: Peer Connections - DONE
- Lab 10: Cleanup - DONE

## Key Learnings
1. Bitcoin nodes communicate over TCP exchanging compact messages
2. Mempool is a waiting room for unconfirmed transactions
3. Miners pick transactions from mempool to include in blocks
4. Merkle trees allow efficient proof of transaction inclusion
5. Bloom filters enable lightweight clients to find transactions
6. Consensus rules are enforced independently by every node
7. BIP152 reduces bandwidth using compact block relay
8. BIP157/158 replaced BIP37 for better privacy
