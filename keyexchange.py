from random import randint


def IsPrime(num):
    for n in range(2,int(num**1/2)+1):
        if num%n==0:
            return False
    return True

def GenerateGenerator():
    return randint(100, 1000)

def GeneratePrime():
    while True:
        numb = randint(100000, 1000000)
        if(IsPrime(numb)):
            prime = numb
            break
    return prime