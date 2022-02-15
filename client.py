from queue import Empty
import socket
import base64

from cryptography.fernet import Fernet
from random import randint
import time
import datetime
import os
from random import randint
from ast import literal_eval

#custom
import keyexchange

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EXCHANGE_MESSAGE = "!EXCHANGE"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
msgCounter = 0
exchangeData = Empty
key = 0
gb = 0

with open('test.txt', 'rb') as file:
    txtfile = file.read()

def generateEncryptionKey():
    b = randint(10000, 100000)
    gb_1 = exchangeData[0] ** b
    global gb
    gb = gb_1%exchangeData[1]

    key_1 = exchangeData[2] ** b
    global key
    key = key_1%exchangeData[1]
    print(key)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(message):
    global msgCounter
    msgCounter = msgCounter + 1
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg = client.recv(2048).decode(FORMAT)
    if(msgCounter == 1):
        global exchangeData
        exchangeData = literal_eval(msg)
        generateEncryptionKey()
    
    print(msg)



def encodeSend(msg):
    send(base64.b64encode(msg))


encodeSend(EXCHANGE_MESSAGE.encode(FORMAT))
encodeSend(str(gb).encode(FORMAT))
encodeSend(txtfile)

input()

encodeSend(DISCONNECT_MESSAGE.encode(FORMAT))