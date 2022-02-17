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
    msg = client.recv(2048).decode(FORMAT)


    if(msgCounter == 1):
        global gb
        data = utility.generateEncryptionKeyClient(literal_eval(msg))
        key = data[0]
        gb = data[1]
        encrypted = True
        print("Communication encrypted: " + str(encrypted))
    else:
        print(msg)


def send(command, data):
    packet = utility.BuildPacket(command, data)
    sendPacket(Fernet(key).encrypt(packet))

def sendUnencrypted(command, data):
    sendPacket(utility.BuildPacket(command, data))

def createConnection():
    sendUnencrypted("EXCHANGE", EXCHANGE_MESSAGE.encode(FORMAT))
    sendUnencrypted("CLPUBKEY", str(gb).encode(FORMAT))

def main():
    input()
    send("DATA", txtfile) 
    input() 
    send("DISCONN", DISCONNECT_MESSAGE.encode(FORMAT))


if __name__ == "__main__":
    createConnection()
    main()