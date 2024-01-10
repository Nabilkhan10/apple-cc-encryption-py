from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_card_number(config, card_number):
    card_number = card_number.replace(" ", "")
    
    public_key = load_pem_public_key(
        config["publicKey"].encode(),
        backend=default_backend()
    )
    
    encrypted = public_key.encrypt(
        card_number.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return {
        "cipherText": base64.b64encode(encrypted).decode('utf-8'),
        "publicKeyHash": config["publicKeyHash"]
    }

card_number = "4242 4242 4242 4242"

encryption_config = {
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvUIrYPRsCjQNCEGNWmSp9Wz+5uSqK6nkwiBq254Q5taDOqZz0YGL3s1DnJPuBU+e8Dexm6GKW1kWxptTRtva5Eds8VhlAgph8RqIoKmOpb3uJOhSzBpkU28uWyi87VIMM2laXTsSGTpGjSdYjCbcYvMtFdvAycfuEuNn05bDZvUQEa+j9t4S0b2iH7/8LxLos/8qMomJfwuPwVRkE5s5G55FeBQDt/KQIEDvlg1N8omoAjKdfWtmOCK64XZANTG2TMnar/iXyegPwj05m443AYz8x5Uw/rHBqnpiQ4xg97Ewox+SidebmxGowKfQT3+McmnLYu/JURNlYYRy2lYiMwIDAQAB\n-----END PUBLIC KEY-----",
    "publicKeyHash": "DsCuZg+6iOaJUKt5gJMdb6rYEz9BgEsdtEXjVc77oAs=",
    "algorithm": "rsa-oaep",
}

encrypted_card_number = encrypt_card_number(encryption_config, card_number)
print(encrypted_card_number)
