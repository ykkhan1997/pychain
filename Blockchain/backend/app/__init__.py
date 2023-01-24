import os
import requests
import random
from flask import Flask,jsonify,request
from backend import pubsub
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import Transaction_Pool
from backend.pubsub import PubSub
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
blockchain=Blockchain()
wallet=Wallet(blockchain)
transaction_pool=Transaction_Pool()
pubsub=PubSub(blockchain,transaction_pool)

@app.route('/blockchain')

def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def mine_block():
    # transcation_data='Stubbed_transcation'
    transaction_data=transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block=blockchain.chain[-1]
    pubsub.broad_cast_block(block)
    transaction_pool.clear_blockchain_transaction(blockchain)
    return jsonify(block.to_json())
     # return jsonify(blockchain.chain[-1].to_json())
@app.route('/wallet/transact',methods=['POST'])
def route_wallet_transact():
    transaction_data=request.get_json()
    transaction=transaction_pool.update_existing_transaction(wallet.address)
    if transaction:
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        
        transaction=Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    pubsub.broad_cast_transaction(transaction)
    print(f'transaction.to_json():{transaction.to_json()}')
    return jsonify(transaction.to_json())

@app.route('/wallet-info')
def wallet_info():
    return jsonify({'address':wallet.address,'balance':wallet.balance})
@app.route('/blockchain/range')
def route_blockchain_range():
    start=int(request.args.get('start'))
    end=int(request.args.get('end'))
    return jsonify(blockchain.to_json()[::-1][start:end])
@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))

@app.route('/known-addresses')
def route_known_addresses():
    known_addresses=set()
    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())
    return jsonify(list(known_addresses))

@app.route('/transactions')
def route_transaction():
    return jsonify(transaction_pool.transaction_data())

ROOT_PORT=5000
PORT=ROOT_PORT
if os.environ.get('PEER')=='True':
    PORT=random.randint(5001,6000)
    
    result=requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    #print(f'result:{result}')
    result_blockchain=Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print(f'\n Successfully synchronize the local chain')
    except Exception as e:
        print(f'--\n Error Synchornizing')
    
if os.environ.get('SEED_DATA')=='True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(),Wallet().address,random.randint(2, 50)).to_json(),
            Transaction(Wallet(),Wallet().address,random.randint(2, 50)).to_json()              
            ])
    for i in range(3):
        transaction_pool.set_transaction(Transaction(Wallet(),Wallet().address,random.randint(2, 50)))
   
    
    
    
    
app.run(port=PORT)