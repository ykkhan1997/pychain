import time
import requests
from backend.wallet.wallet import Wallet

'''Import request is used to handle the http requests'''

BASE_URL='http://localhost:5000'
def get_blockcahin():
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blockcahin_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transact(recipient,amount):
    return requests.post(f'{BASE_URL}/wallet/transact',
    json={'recipient':recipient,'amount':amount}
    ).json()
    
def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

recipient=Wallet().address

transact_1=post_wallet_transact(recipient, 15)
print(f'\ntransact_1: {transact_1}\n')
time.sleep(1)
transact_2=post_wallet_transact(recipient, 30)
print(f'\ntransact_: {transact_2}\n')
time.sleep(1)
mined_block=get_blockcahin_mine()
print(f'mined_block: {mined_block}')
time.sleep(1)
wallet_info=get_wallet_info()
print(f'\nwallet_info: {wallet_info}\n')

start_blockchain=get_blockcahin()
# print(f'start_blockchain: {start_blockchain}')