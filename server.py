from queue import Empty
import socket 
import threading

from cryptography.fernet import Fernet


# custom
import utility.keyexchange as keyexchange
import utility.utility as utility
# Generate part Key
g = keyexchange.GenerateGenerator()
n = keyexchange.GenerateBigNumber()
a = keyexchange.GenerateGenerator()
ga_1 = g ** a
ga = ga_1%n
exchangeData = [g, n, ga]
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_COMMAND = "DISCONN"
EXCHANGE_COMMAND = "EXCHANGE"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    clientExchangeKey = False
    encrypted = False
    key = Empty
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            if not encrypted:
                msg = utility.ExtractPacket(msg)
            
            
            if(encrypted):
                msg = Fernet(key).decrypt(msg)
                msg = utility.ExtractPacket(msg)

            command = msg[0]
            data = msg[1]
            
            if command == DISCONNECT_COMMAND:
                print(f"CLIENT {addr} DISCONNECTED")
                connected = False
            elif(clientExchangeKey):
                key = utility.generateEncryptionKey(data, a, n)
                encrypted = True
                print("Communication encrypted: " + str(encrypted))
                clientExchangeKey = False
            elif command == EXCHANGE_COMMAND:
                conn.send(str(exchangeData).encode(FORMAT))
                clientExchangeKey = True
            else:
                print(data)
            conn.send("Msg received".encode(FORMAT))
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


