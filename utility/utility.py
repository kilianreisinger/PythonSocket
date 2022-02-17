import base64
from queue import Empty
import utility.keyexchange as keyexchange


##  ----------  General Utility ---------- 
def BS64encode(data):
    return base64.b64encode(data)

def BS64decode(data):
    return base64.b64decode(data)

def UTFencode(data):
    return data.encode("utf-8")

def UTFdecode(data):
    return data.decode("utf-8")

def mergeList(list):
    return "@@@@".join(map(str, list))

def splitList(list):
    data = list.decode("utf-8").split("@@@@")
    return data

def buildHeader(message, HEADER, FORMAT):
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length

def ExpandHeader(command):
    command = str.encode(command)
    commandLen = len(command)
    lendDiff = 8 - commandLen
    command += b' ' * lendDiff
    if(len(command) > 8):
        print("##### !!! ERROR:  OVER 8 Bytes !!! #####")
        exit()
    return command




##  ----------   Packet Building  ----------

def IsByte(data):
    if(type(data) == type(b'')):
        return True
    else:
        return False

def BuildPacket(command, data):
    command = ExpandHeader(command)
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





###  ----------   ENCRYPTION  ----------
## SERVER
def generateEncryptionKey(gb, a, n):
    key_1 = int(gb) ** a
    key =  key_1%n
    key = key.to_bytes(32,'big')
    return bytes(base64.urlsafe_b64encode(key))

## CLIENT
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


###  ----------   FILE HANDLING  ----------

def appendFileInfo(data, filetype, name):
    header = ExpandHeader(filetype)
    lenght = len(data).to_bytes(8,'big')
    return header + lenght + data + BS64encode(UTFencode(name))

def extractFile(data):
    filetype = data[:8]
    length = int.from_bytes(data[8:16], "big") + 16
    payload = data[16:length]
    filename = BS64decode(data[length:])
    return filetype, payload, filename

def saveFile(data):
    extraced = extractFile(data)
    filetype = extraced[0]
    filetype = UTFdecode(filetype).replace(" ", "")  
    file = extraced[1]
    filename =  UTFdecode(extraced[2])

    path = "./ServerStorage/"
    filetoSave = path + filename + "." +filetype
    print(filetoSave)
    with open(filetoSave, 'wb') as dec_file:
        dec_file.write(file)



   