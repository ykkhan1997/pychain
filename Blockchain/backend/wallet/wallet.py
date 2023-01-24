
import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import(
    encode_dss_signature,
    decode_dss_signature
)
class Wallet:
    '''An Individual wallet for a miner
       keep track of the miner's balance
       Allow a miner to authorize transcations'''
    def __init__(self,blockchain=None):
        self.blockchain=blockchain
        self.address=str(uuid.uuid4())[0:8]
        # self.balance=STARTING_BALANCE
        self.private_key=ec.generate_private_key(ec.SECP256K1(),default_backend())
        self.public_key=self.private_key.public_key()
        self.serialize_public_key()
        
    @property
    def balance(self):
        return Wallet.Calculate_balance(self.blockchain, self.address)
        
    def sign(self,data):
        '''Generate the signature based on the data by using local private key'''
        return decode_dss_signature( self.private_key.sign(json.dumps(data).encode('utf-8'),
        ec.ECDSA(hashes.SHA256())))
    def serialize_public_key(self):
        '''Reset the public key to its serialize version
            Below line the combination of encoding and format will successfully
            transform the public key into a binary
            PEM is a common itself coding to use with in the field of security'''
        
        # self.public_key_bytes=self.public_key.public_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PublicFormat.SubjectPublicKeyInfo
        # )
        # # print(f'public_key_bytes: {self.public_key_bytes}')
        
        # decode_public_key=self.public_key_bytes.decode('utf-8')
        # # print(f'decode_public_key: {decode_public_key}')
        # self.public_key=decode_public_key
        self.public_key=self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
    @staticmethod
    def verify(public_key,data,signature):
        '''Verify a signature based on the original public key and data'''
        deserialize_public_key=serialization.load_pem_public_key(
        public_key.encode('utf-8'),
        default_backend()    
        )
        (r,s)=signature
        # print(f'\n signature: {signature}\n')
        try:
            deserialize_public_key.verify(
                encode_dss_signature(r,s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
        
    @staticmethod
    def Calculate_balance(blockchain,address):
        '''Calculate the balance of the blockchain considering the transaction data with in the blockchain
        The address can be find by adding the output values that belong to the address since the most recent
        transaction by that transaction'''
        balance=STARTING_BALANCE
        if not blockchain:
            return balance
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address']==address:
                    #Any time address conduct a new transaction it reset its balance
                    balance=transaction['output'][address]
                elif address in transaction['output']:
                    balance+=transaction['output'][address]
                        
        return balance
               
    
def main():
    wallet=Wallet()
    print(f'wallet:{wallet.__dict__}')
    data={'foo':'bar'}
    signature=wallet.sign(data)
    print(f'signature: {signature}')
    should_be_valid=Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_verify: {should_be_valid}')
    should_not_be_valid=Wallet.verify(Wallet().public_key, data, signature)
    print(f'_should_not_be_valid: {should_not_be_valid}')
    
if __name__=='__main__':
    main()
           