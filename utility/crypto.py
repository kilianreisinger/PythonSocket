from cryptography.fernet import Fernet

def encrypt(data, fernet):
    return fernet.encrypt(data)
def decrypt(data, fernet):
    return fernet.decrypt(data)