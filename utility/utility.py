import base64
from email import contentmanager
from struct import pack
import utility.keyexchange as keyexchange


## General Utility
def BS64encode(data):
    return base64.b64encode(data)

def BS64decode(data):
    return base64.b64decode(data)


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
    if not IsByte(data):
       data = data.encode("utf-8") 
    
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


