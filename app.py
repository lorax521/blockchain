from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/')
def index():
    return {'index': 'Weclome to the Fable Blockchain API'}

@app.route('/mine', methods=['GET'])
def mine():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {
        'msg': 'Congrats! You just mined a block and it has been added to the blockchain!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previousHash': block['previousHash']
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def getChain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200

@app.route('/valid', methods=['GET'])
def isChainValid():
    response = {
        'valid': blockchain.isChainValid(blockchain.chain)
    }
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000, debug=True)