import base64
from queue import Empty

FORMAT = 'utf-8'


def BS64encode(msg):
    return base64.b64encode(msg)
def BS64decode(msg):
    return base64.b64decode(msg)

with open('ClientStorage/test.jpg', 'rb') as file:
    txtfile = file.read()


COMAND = str.encode("EXCHANGE")
# CONTENT = str.encode("Dies ist mein Kontent")
CONTENT = txtfile
LENGTH = len(CONTENT).to_bytes(8,'big')

COMBINED = COMAND + LENGTH + CONTENT

COMBINED = BS64encode(COMBINED)

COMBINED = BS64decode(COMBINED)


COMAND = COMBINED[:8]
HEADER2 = COMBINED[8:16]
LENGHT = int.from_bytes(HEADER2, "big") + 16
CONTENT = COMBINED[16:LENGHT]


print(str(COMBINED) + "  Combined Byte with lenght of: " + str(len(COMBINED)))
print(COMAND.decode(FORMAT))
print(int.from_bytes(HEADER2, "big"))
print(BS64encode(CONTENT))

with open('ServerStorage/transfer.jpg', 'wb') as dec_file:
    dec_file.write(CONTENT)