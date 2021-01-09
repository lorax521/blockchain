from flask import Flask, jsonify, request
import requests

from datetime import datetime
import hashlib
import json
from urllib.parse import urlparse
import numpy as np

class CryptoCoin:
    def __init__(self):
        self.name = 'cryptocoin'
        self.transactions = []
        self.chain = []
        self.createBlock(proof=1, previousHash='0') # create genesis block
        self.leadingZeros = '0000'
        self.nodes = set()

    def createBlock(self, proof, previousHash, data='null'):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'previousHash': previousHash,
            'data': data,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def getPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            # more leading zeros makes the problem harder to solve
            if hashOperation.startswith(self.leadingZeros):
                checkProof = True
            else:
                newProof += 1
        return newProof

    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if not hashOperation.startswith(self.leadingZeros):
                return False
            previousBlock = block
            blockIndex += 1
        return True

    def addTransaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previousBlock = self.getPreviousBlock()
        return previousBlock['index'] + 1

    def addNode(self, address):
        parsedAddress = urlparse(address)
        self.nodes.add(parsedAddress.netloc)

    def replaceChain(self):
        network = self.nodes
        longestChain = None
        maxLength = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if lenth > maxLength and self.isChainValid(chain):
                    maxLength = length
                    longestChain = chain
        if longestChain:
            self.chain = longestChain
            return True
        return False