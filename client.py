from queue import Empty
import socket
import base64

from cryptography.fernet import Fernet
from ast import literal_eval
import utility.utility as utility
from cryptography.fernet import Fernet

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_COMMAND = "DISCONN"
EXCHANGE_COMMAND = "EXCHANGE"
PUBKEY_COMMAND = "CLPUBKEY"
DATA_COMMAND = "DATA"
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

def sendPacket(message):
    global key
    global encrypted
    global msgCounter
    msgCounter = msgCounter + 1

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


    print(" --- DATA SENT waiting for response ---")
    msg = client.recv(2048)
    print(" --- RESPONSE RECEIVED ---")
    
    if(encrypted):
        msg = Fernet(key).decrypt(msg)
    msg = utility.ExtractPacket(msg)
            
    command = msg[0]
    data = msg[1]
    if command == EXCHANGE_COMMAND:
        global gb
        data = utility.generateEncryptionKeyClient(utility.splitList(data))
        key = data[0]
        gb = data[1]
        encrypted = True
        print("Communication encrypted: " + str(encrypted))
    if command == DATA_COMMAND:
        print(msg)


def send(command, data=Empty):
    packet = utility.BuildPacket(command, data)
    sendPacket(Fernet(key).encrypt(packet))

def sendUnencrypted(command, data=Empty):
    sendPacket(utility.BuildPacket(command, data))


def createConnection():
    input()
    sendUnencrypted(EXCHANGE_COMMAND)
    input()
    sendUnencrypted(PUBKEY_COMMAND, str(gb).encode(FORMAT))

def main():
    input()
    send(DATA_COMMAND, txtfile) 
    input() 
    send(DISCONNECT_COMMAND)


if __name__ == "__main__":
    createConnection()
    main()