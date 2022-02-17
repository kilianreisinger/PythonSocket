from cryptography.fernet import Fernet
import utility.utility as utility

packet = utility.BuildPacket("EXCHANGE", "This is the content")
packetData = utility.ExtractPacket(packet)

print(packet)
print(packetData)


key = Fernet.generate_key()
fernet = Fernet(key)

encrypted = fernet.encrypt(packet)

print(encrypted)


