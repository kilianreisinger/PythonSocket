from ctypes import util
from queue import Empty
import socket
import base64

from cryptography.fernet import Fernet
from random import randint
from random import randint
from ast import literal_eval
import utility.utility as utility
import utility.crypto as crypto 
from cryptography.fernet import Fernet

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EXCHANGE_MESSAGE = "!EXCHANGE"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
msgCounter = 0


## Encryption Global VARS
exchangeData = Empty
global key
key = 0
gb = 0
encrypted = False

## Testing File OPEN
with open('ClientStorage/test.txt', 'rb') as file:
    txtfile = file.read()



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(message):
    global key
    global encrypted
    global msgCounter
    msgCounter = msgCounter + 1

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg = client.recv(2048).decode(FORMAT)


    if(msgCounter == 1):
        global gb
        data = utility.generateEncryptionKeyClient(literal_eval(msg))
        key = data[0]
        gb = data[1]
        encrypted = True
        print("Communication encrypted: " + str(encrypted))
    else:
        print("")


def encodeSend(msg):
    send(base64.b64encode(msg))

def createConnection():
    encodeSend(EXCHANGE_MESSAGE.encode(FORMAT))
    encodeSend(str(gb).encode(FORMAT))
    
def main():
    input()
    encodeSend(crypto.encrypt(txtfile,Fernet(key))) 
    input()
    encodeSend(crypto.encrypt(DISCONNECT_MESSAGE.encode(FORMAT),Fernet(key))) 


if __name__ == "__main__":
    createConnection()
    main()