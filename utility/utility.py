import base64
import utility.keyexchange as keyexchange


## General Utility
def BS64decode(msg, FORMAT):
    encode = base64.b64decode(msg)
    encode2 = encode.decode(FORMAT)
    return encode2



## ENCRYPTION
## SERVER
def generateEncryptionKey(gb, a, n):
    key_1 = int(gb) ** a
    key =  key_1%n
    key = key.to_bytes(32,'big')
    return base64.urlsafe_b64encode(key)

##CLIENT
## Generate Encryption KEY
def generateEncryptionKeyClient(exchangeData):
    b = keyexchange.GenerateGenerator()
    gb_1 = exchangeData[0] ** b
    global gb
    gb = gb_1%exchangeData[1]

    key_1 = exchangeData[2] ** b
    key = key_1%exchangeData[1]
    key = key.to_bytes(32,'big')
    key = base64.urlsafe_b64encode(key)
    return key, gb