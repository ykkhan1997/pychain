
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
def test_verify_valid_signature():
    wallet=Wallet()
    data={'foo':'bar'}
    signature=wallet.sign(data)
    
    assert Wallet.verify(wallet.public_key,data,signature) 
    
    
def test_verify_invalid_signature():
    wallet=Wallet()
    data={'foo':'bar'}
    signature=wallet.sign(data)
    
    Wallet.verify(Wallet().public_key,data,signature)
    
def test_Calculate_balance():
   wallet=Wallet()
   blockchain=Blockchain()
   Wallet.Calculate_balance(blockchain, wallet.address) ==STARTING_BALANCE
   
   amount=25
   
   transaction=Transaction(wallet,'receipient',amount)
   
   blockchain.add_block([transaction.to_json()])
   
   Wallet.Calculate_balance(blockchain, wallet.address)==STARTING_BALANCE - amount
   
   received_amount_1=5
   received_transaction_1=Transaction(
        Wallet(),
        wallet.address,
        received_amount_1
    )
   received_amount_2=5
   received_transaction_2=Transaction(
        Wallet(),
        wallet.address,
        received_amount_2
    )   
   blockchain.add_block([received_transaction_1.to_json(),received_transaction_2.to_json()])   
   Wallet.Calculate_balance(blockchain, wallet.address)==STARTING_BALANCE \
       - amount +received_amount_1, received_amount_2
    