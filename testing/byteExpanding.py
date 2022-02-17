
FORMAT = 'utf-8'


COMMAND = str.encode("PUSH")
HEADER = 8

COMMANDLEN = len(COMMAND)
LENDIFF = 8 - COMMANDLEN
COMMAND += b' ' * LENDIFF
COMMAND = COMMAND.decode(FORMAT).replace(" ", "") 
print(COMMAND.encode(FORMAT))
