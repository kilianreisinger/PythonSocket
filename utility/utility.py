import base64
from queue import Empty
import utility.keyexchange as keyexchange


## General Utility
def BS64encode(data):
    return base64.b64encode(data)

def BS64decode(data):
    return base64.b64decode(data)

def mergeList(list):
    return "@@@@".join(map(str, list))

def splitList(list):
    data = list.decode("utf-8").split("@@@@")
    return data

##  ----------   Packet Building  ----------

def ExpandHeaderCommand(command):
    command = str.encode(command)
    commandLen = len(command)
    lendDiff = 8 - commandLen
    command += b' ' * lendDiff
    if(len(command) > 8):
        print("##### !!! ERROR: COMMAND OVER 8 Bytes !!! #####")
        exit()
    return command

def IsByte(data):
    if(type(data) == type(b'')):
        return True
    else:
        return False

def BuildPacket(command, data):
    command = ExpandHeaderCommand(command)
    if(data == Empty):
        data = b''

    if not IsByte(data):
        isList = isinstance(data, list)
        if not isList:
            data = data.encode("utf-8") 
        else:
            data = mergeList(data).encode("utf-8")
    
    lenght = len(data).to_bytes(8,'big')
    packet = command + lenght + data
    return BS64encode(packet)




##  ----------   Packet Extraction  ----------

def ExtractPacket(packet):
    packet = BS64decode(packet)
    command = packet[:8]
    command = command.decode("utf-8").replace(" ", "") 
    length = int.from_bytes(packet[8:16], "big") + 16
    content = packet[16:length]

    return command, content



##  ----------   ENCRYPTION  ----------
## SERVER
def generateEncryptionKey(gb, a, n):
    key_1 = int(gb) ** a
    key =  key_1%n
    key = key.to_bytes(32,'big')
    return bytes(base64.urlsafe_b64encode(key))

##CLIENT
## Generate Encryption KEY
def generateEncryptionKeyClient(exchangeData):
    b = keyexchange.GenerateGenerator()
    gb_1 = int(exchangeData[0]) ** b
    global gb
    gb = gb_1%int(exchangeData[1])
    key_1 = int(exchangeData[2]) ** b
    key = key_1%int(exchangeData[1])
    key = key.to_bytes(32,'big')
    key = base64.urlsafe_b64encode(key)
    return key, gb


