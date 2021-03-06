from queue import Empty
import socket
import threading
from datetime import datetime
from cryptography.fernet import Fernet


# custom
import utility.utility as utility
import COMMANDS as CM
import utility.numberGenerator as numGen

# Generate part Key
g = numGen.GenerateGenerator()
n = numGen.generatePrime(160)
a = numGen.GenerateGenerator()
ga_1 = g ** a
ga = ga_1%n
exchangeData = [g, n, ga]
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
OKMSG = "200 OK"



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def sendUnencrypted(command, conn, data=Empty):
    conn.send(utility.BuildPacket(command, data))

def send(command, key, conn, data=Empty):
    packet = utility.BuildPacket(command, data)
    conn.send(Fernet(key).encrypt(packet))  

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    encrypted = False
    key = Empty
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)

            if(encrypted):
                msg = Fernet(key).decrypt(msg)
            msg = utility.ExtractPacket(msg)

            
            command = msg[0]
            data = msg[1]
            if command == CM.DISCONNECT_COMMAND:
                print(f"CLIENT {addr} DISCONNECTED")
                connected = False
            if command == CM.PUBKEY_COMMAND:
                key = utility.generateEncryptionKey(data, a, n)
                send(CM.STATUS_COMMAND,key , conn)
                encrypted = True
                print("Communication encrypted: " + str(encrypted))
            if command == CM.EXCHANGE_COMMAND:
                sendUnencrypted(CM.EXCHANGE_COMMAND, conn, exchangeData)

            if command == CM.DATA_ASCI_COMMAND:
                print(utility.UTFdecode(data))
                send(CM.DATA_ASCI_COMMAND, key, conn, OKMSG)

            if command == CM.DATA_FILE_COMMAND:
                print("SAVING FILE (" +  str(datetime.now()) + ")")
                utility.saveFile(data)
                print("DONE SAVING FILE (" +  str(datetime.now()) + ")")
                send(CM.DATA_ASCI_COMMAND, key, conn, OKMSG)
            
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

if __name__ == "__main__":
    start()


