import socket 
import threading
import base64

from cryptography.fernet import Fernet
from random import randint
import time
import datetime
import os

# custom
import keyexchange

# Generate part Key
g = keyexchange.GenerateGenerator()
n = keyexchange.GeneratePrime()
a = randint(10000, 100000)
ga_1 = g ** a
ga = ga_1%n
exchangeData = [g, n, ga]

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
EXCHANGE_MESSAGE = "!EXCHANGE"
key = 0


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def generateEncryptionKey(gb):
    print(gb)
    # key_1 = int(gb) ** a
    # global key
    # key = key_1%n
    # print(key)


def BS64decode(msg):
    encode = base64.b64decode(msg)
    encode2 = encode.decode(FORMAT)
    return encode2

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    clientExchangeKey = False
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            msg = BS64decode(msg)
            # msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if(clientExchangeKey):
                generateEncryptionKey(msg)
                clientExchangeKey = False
            if msg == EXCHANGE_MESSAGE:
                conn.send(str(exchangeData).encode(FORMAT))
                clientExchangeKey = True
            else:
            # print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))
            print(msg)
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()