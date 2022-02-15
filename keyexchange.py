from random import randint
import math


def IsPrime(num):
    for n in range(2,int(num**1/2)+1):
        if num%n==0:
            return False
    return True

def GenerateGenerator():
    return randint(100, 1000)

def GeneratePrime():
    numb = randint(1000000, 10000000)
    while True:
        if(IsPrime(numb)):
            prime = numb
            break
        else: 
            numb = numb + 1

    return prime

def primeSieve(sieveSize):
    sieve = [True] * sieveSize
    sieve[0] = False # zero and one are not prime numbers
    sieve[1] = False


    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i
        
        primes = []

        for i in range(sieveSize):
            if sieve[i] == True:
                primes.append(i)
        return primes