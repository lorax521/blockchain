from datetime import datetime
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.name = 'Fable'
        self.chain = []
        self.createBlock(proof=1, previousHash='0')
        self.leadingZeros = '0000'

    def createBlock(self, proof, previousHash, data='null'):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'previousHash': previousHash,
            'data': data
        }
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

        