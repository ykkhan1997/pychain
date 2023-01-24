from backend.util.crypto_hash import crypto_hash


def test_crypto_hash():
    
    assert crypto_hash('abc','def',[1])==crypto_hash('abc',[1],'def')