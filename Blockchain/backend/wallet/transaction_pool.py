
class Transaction_Pool:
    
    def __init__(self):
        self.transaction_map={}
        '''A map in programming collect of key,value pairs'''
        
    def set_transaction(self,transaction):
        '''Set the transaction in the transaction pool'''
        
        self.transaction_map[transaction.id]=transaction
        
    def update_existing_transaction(self,address):
        '''Find a transaction generated by the address in transaction pool'''
        for transaction in self.transaction_map.values():
            if transaction.input['address']==address:
                return transaction
    def transaction_data(self):
        '''Return the transaction of the transaction pool represented in their json serialize form'''
        return list(map(
            lambda transaction:transaction.to_json(), 
            self.transaction_map.values()
        ))
        # transaction_values=transaction_pool.transaction_map.values()
        # transaction_data=list(map(lambda transaction:transaction.to_json(),transaction_values))
        # return transaction_data
    def clear_blockchain_transaction(self,blockchain):
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass