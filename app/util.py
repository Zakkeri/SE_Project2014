from os import urandom
from Crypto.Hash import SHA256  

from binascii import hexlify
from string import digits, uppercase
from random import randint

alphanumeric = digits + uppercase

def genvin():
    
    return "".join([alphanumeric[randint(0,len(alphanumeric))]
                  for x in range(17)])

def getsalt():
    return hexlify(urandom(16))

def createhash(salt, password):
    
    thehash = SHA256.new(salt + password)

    return thehash.hexdigest()

if __name__ == "__main__":
    print genvin()
    print genvin()
