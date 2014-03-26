from os import urandom
from Crypto.Hash import SHA256  

from binascii import hexlify

def getsalt():
    return hexlify(urandom(16))

def createhash(salt, password):
    
    thehash = SHA256.new(salt + password)

    return thehash.hexdigest()

