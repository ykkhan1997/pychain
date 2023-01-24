from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction_pool import Transaction_Pool
from backend.wallet.wallet import Wallet


def test_transaction_pool():
    transaction_pool=Transaction_Pool()
    transaction=Transaction(Wallet(), 'recipient', 50)
    transaction_pool.set_transaction(transaction)
    
    assert transaction_pool.transaction_map[transaction.id]==transaction
    
def test_clear_blockchain_transaction():
    transaction_pool=Transaction_Pool()
    blockchain=Blockchain()
    transaction_1=Transaction(Wallet(),'recipient',1)
    transaction_2=Transaction(Wallet(),'recipient',2)
    
    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)
    
   
    blockchain.add_block([transaction_1.to_json(),transaction_2.to_json()])
    
    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map
    
    transaction_pool.clear_blockchain_transaction(blockchain)
    assert not transaction_1.id in transaction_pool.transaction_map
    assert not transaction_2.id in transaction_pool.transaction_map
    
    
    
    