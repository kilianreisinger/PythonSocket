import base64

with open('test.txt', 'rb') as file:
    original = file.read()
    
# msg = original.encode("utf-8")
msg = base64.b64encode(original)
print(msg)
msgdecoded = base64.b64decode(msg)
# msgdecoded = msgdecoded.decode("utf-8")
print(msgdecoded)