from textwrap import dedent
from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import BlockChain
import json


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    return 'We will mine new block'


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'One of required keys is missing', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)