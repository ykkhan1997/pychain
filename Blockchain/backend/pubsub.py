import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.wallet.transaction import Transaction
from backend.blockchain.block import Block

pnconfig=PNConfiguration()
pnconfig.subscribe_key='sub-c-4ab2851d-6334-46ca-86f9-157b1c2efd53'
pnconfig.publish_key='pub-c-68ee9821-af71-4613-90af-39f8c4442ac2'


# TEST_CHANNEL='TEST_CHANNEL'
# BLOCK_CHANNEL='BLOCK_CHANNEL'
CHANNEL={
    'TEST':'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION':'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self,blockchain,transaction_pool):
        self.blockchain=blockchain
        self.transaction_pool=transaction_pool
    
    def message(self,pubnub,message_object):
        print(f'\n --Channel : {message_object.channel} |Message: {message_object.message}')
        if message_object.channel==CHANNEL['BLOCK']:
            block=Block.from_json(message_object.message)
            potential_chain=self.blockchain.chain[:]
            potential_chain.append(block)
            try:    
                self.blockchain.replace_chain(potential_chain)
                print(f'\n successfully replace the local chain')
                self.transaction_pool.clear_blockchain_transaction(
                    self.blockchain
                )
            except Exception as e:
                print(f'\n Did not replace chain: {e}')
        elif message_object.channel==CHANNEL['TRANSACTION']:
            transaction=Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'\n Set the new transaction in the transaction pool')

class PubSub():
    '''Handles the publish/subscribe layer of the application.
    Provide communication between the node of the blockchain network'''
    def __init__(self,blockchain,transaction_pool) -> None:
        self.pubnub=PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNEL.values()).execute()
        self.pubnub.add_listener(Listener(blockchain,transaction_pool))
        
    def publish(self,channel,message):
        '''Publish the message object to the channel'''
        self.pubnub.publish().channel(channel).message(message).sync()
    
    def broad_cast_block(self,block):
        '''broadcast block object to all nodes'''
        self.publish(CHANNEL['BLOCK'],block.to_json())
    
    def broad_cast_transaction(self,transaction):
        '''Set the transaction to all nodes'''
        self.publish(CHANNEL['TRANSACTION'], transaction.to_json())
    


def main():
    pubsub=PubSub()
    time.sleep(1)
    pubsub.publish(CHANNEL['TEST'],{'foo':'bar'})
    
if __name__=='__main__':
    main()
