from struct import pack
import utility.utility as utility

packet = utility.BuildPacket("EXCHANGE", "This is the content")
packetData = utility.ExtractPacket(packet)

print(packet)
print(packetData)