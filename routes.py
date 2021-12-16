import sys

from uuid import uuid4

from flask import Flask
from flask.globals import request
from flask.json import jsonify

from blockchain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
bc = Blockchain()

@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': bc.chain,
        'length': len(bc.chain)
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine_block():
    bc.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    last_block_hash = bc.hash_block(bc.last_block)
    index = len(bc.chain)
    nonce = bc.proof_of_work(index, last_block_hash, bc.current_transactions)
    block = bc.append_block(nonce, last_block_hash)
    response = {
        'message': 'New block added',
        'index': block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transaction': block['transaction']
    }
    return jsonify(response), 200

@app.route('/new-transaction', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required_fields):
        return ('Missing fields', 422)

    index = bc.add_transaction(values['sender'], values['recipient'], values['amount'])
    response = {
        'message': f'Transaction will be added to block {index}'
    }
    return jsonify(response), 201

@app.route('/add-node', methods=['POST'])
def add_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return ('Missing node info', 422)
    for node in nodes:
        bc.add_node(node)
    response = {
        'message': f'New nodes added',
        'nodes': list(bc.nodes)
    }
    return jsonify(response), 201

@app.route('/node-sync', methods=['GET'])
def node_sync():
    updated = bc.update_blockchain();
    if updated:
        response = {
            'message': f'Chain synced with the latest',
            'blockchain': bc.chain
        }
    else:
        response = {
            'message': f'Chain already synced with the latest',
            'blockchain': bc.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))