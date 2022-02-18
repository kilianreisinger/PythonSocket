from queue import Empty
import socket
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet

## custom
import utility.utility as utility
import COMMANDS as CM

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
PROG = "\n press ENTER"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

## Encryption Global VARS
exchangeData = Empty
key = 0
gb = 0
encrypted = False

## Testing File OPEN
with open('ClientStorage/test.txt', 'rb') as file:
    txtfile = file.read()
with open('ClientStorage/test.jpg', 'rb') as file:
    imgfile = file.read()



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def sendPacket(message):
    global key
    global encrypted

    ## SENDING DATA
    client.send(utility.buildHeader(message, HEADER, FORMAT))
    client.send(message)

    

    ## RECEIVE DATA
    msg = client.recv(2048)
    
    ## decrypt if communication is encrypted
    if(encrypted):
        msg = Fernet(key).decrypt(msg)
    msg = utility.ExtractPacket(msg)
    command = msg[0]
    data = msg[1]


    if command == CM.EXCHANGE_COMMAND:
        global gb
        data = utility.generateEncryptionKeyClient(utility.splitList(data))
        key = data[0]
        gb = data[1]
        encrypted = True
        print("Communication encrypted: " + str(encrypted))
    
    
    if command == CM.DATA_ASCI_COMMAND:
        print(data)


def send(command, data=Empty):
    packet = utility.BuildPacket(command, data)
    sendPacket(Fernet(key).encrypt(packet))

def sendUnencrypted(command, data=Empty):
    sendPacket(utility.BuildPacket(command, data))


def createConnection():
    input(PROG)
    sendUnencrypted(CM.EXCHANGE_COMMAND)
    input(PROG)
    sendUnencrypted(CM.PUBKEY_COMMAND, str(gb).encode(FORMAT))

def main():
    input(PROG)
    send(CM.DATA_ASCI_COMMAND, txtfile) 
    input(PROG)
    send(CM.DATA_FILE_COMMAND, utility.appendFileInfo(imgfile, "jpg", "myfile2"))
    input(PROG)
    send(CM.DISCONNECT_COMMAND)


if __name__ == "__main__":
    createConnection()
    main()