from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARDS_INPUT,MINING_REWARDS
class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        
        return f'Blockchain:{self.chain}'
    
    
    def replace_chain(self,chain):
        '''Replace the local chain with the incoming one if the following rule applies
        -The incoming chain is longer than the local one
        -The incoming chain must be formatted correctly'''
        if len(chain)<=len(self.chain):
            raise Exception('Cannot replace.The incoming chain must be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace.The incoming chain is invalid:{e}')
        self.chain=chain
    def to_json(self):
        # '''serialize the blockhcain into a list of blocks'''
        # serialize_chain=[]
        # for block in self.chain:
        #     serialize_chain.append(block.to_json())
        # return serialize_chain
        return list(map(lambda block:block.to_json(),self.chain))
    @staticmethod
    def from_json(chain_json):
        '''Deserialize a list of blocks into a Blockchain instance.
        The result will contain a chain of list of block instances'''
        blockchain=Blockchain()
        blockchain.chain=list(map(lambda block_json:Block.from_json(block_json),chain_json)
        )
        return blockchain
        
    
    @staticmethod
    def is_valid_chain(chain):
        '''Validate the blockchain
        Encofce the following rules of the blockchain
        -The chain must start with the genesis block
        -The block must be formatted correctly'''
        if chain[0]!=Block.genesis():
            raise Exception('The genesis block must be correct')
        for i in range(1,len(chain)):
            block=chain[i]
            last_block=chain[i-1]
            Block.is_valid_block(last_block,block)  
            Blockchain.is_valid_transaction_chain(chain)
    @staticmethod
    def is_valid_transaction_chain(chain):
        '''Enforce the rule of chain composed of blocks of transaction
            -Each transaction must only appear one time
            -There can be only one mining reward per block
            -Each transaction must be valid'''
            
        transaction_ids=set()
        for i in range(len(chain)):
            block=chain[i]
            has_mining_reward=False
            for transaction_json in block.data:
                transaction=Transaction.from_json(transaction_json)
                  
                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')
                
                transaction_ids.add(transaction.id)
                if transaction.input==MINING_REWARDS_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can be only one mining reward per block'
                            f'Check block with hash {block.hash}'
                        )
                    has_mining_reward=True
                else:
                
                    historic_blockchain=Blockchain()
                    historic_blockchain.chain=chain[0:i]
                    historic_balance=Wallet.Calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )
                    
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid input amount')
                    
                     
                    Transaction.is_valid_transaction(transaction)
            

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    
    

    print(blockchain)
    print(f'blockchain.py ___name__: {__name__}')

if __name__ == '__main__':
    main()