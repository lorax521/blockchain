from flask import Flask, jsonify
from cryptocoin import CryptoCoin
from uuid import uuid4 as uuid

app = Flask(__name__)

blockchain = CryptoCoin()
nodeAddress = str(uuid()).replace('-', '')

@app.route('/')
def index():
    return {'index': 'Weclome to the CryptoCoin API'}

@app.route('/mine', methods=['GET'])
def mine():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    # TODO update receiver and amount
    blockchain.addTransaction(sender=nodeAddress, receiver='Dogfish', amount=1)
    block = blockchain.createBlock(proof, previousHash)
    response = {
        'msg': 'Congratulations! You just mined a block and it has been added to the blockchain!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previousHash': block['previousHash'],
        'transactions': block['transactions'],

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

@app.reoute('/addTransaction', methods = ['POST'])
def addTransaction():
    json = request.get_json()
    transactionKeys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transactionKeys):
        return jsonify({'Warning': 'Not all the required keys were included in the request'}), 400
    index = blockchain.addTransaction(sender=json['sender'], receiver=json['receiver'], amount=json['amount'])
    return jsonify({'Message': f'The transaction has been added to the block {index}'}), 201

app.run(host='0.0.0.0', port=5000, debug=True)