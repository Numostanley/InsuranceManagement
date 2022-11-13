from core.settings import base
from jose import jws
from cryptography.hazmat.primitives import serialization as crypto_serialization
import time

def docusign_token():
    iat = time.time()
    exp = iat+(3600*24)
    payload = {
        "sub": base.client_user_id,
        "iss": base.CLIENT_AUTH_ID,
        "iat": iat, # session start_time
        "exp": exp, # session end_time
        "aud":"account-d.docusign.com",
        "scope":"signature"
    }
    
    with open('docusign.pem', "rb") as key_file:
       private_key = crypto_serialization.load_pem_private_key(key_file.read(), password=None)
       
    key = private_key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
    jwt_token = jws.sign(payload, key, algorithm='RS256')
     
    return jwt_token
