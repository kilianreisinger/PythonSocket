from cryptography.fernet import Fernet
import utility.utility as utility


list = [324234,234234234,2342344]
merge = utility.mergeList(list)
split = utility.splitList(merge)
print(split)


exit()

packet = utility.BuildPacket("EXCHANGE", "This is the content")
packetData = utility.ExtractPacket(packet)

print(packet)
print(packetData)


key = Fernet.generate_key()
fernet = Fernet(key)

encrypted = fernet.encrypt(packet)

print(encrypted)


