from cryptography.fernet import Fernet
import utility.utility as utility


## Testing file type appender (file type header)
with open('ClientStorage/test.jpg', 'rb') as file:
    imgfile = file.read()

payload = utility.appendFileInfo(imgfile, "jpg", "myfile")

extraced = utility.extractFile(payload)

utility.saveFile(payload)
exit()

## Testing EXCHANGE data merger and splitter
list = [324234,234234234,2342344]
merge = utility.mergeList(list)
split = utility.splitList(merge)
print(split)


exit()

## Testing Packet Builder with encryption
packet = utility.BuildPacket("EXCHANGE", "This is the content")
packetData = utility.ExtractPacket(packet)

print(packet)
print(packetData)


key = Fernet.generate_key()
fernet = Fernet(key)

encrypted = fernet.encrypt(packet)

print(encrypted)


