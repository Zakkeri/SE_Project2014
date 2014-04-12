#==============================================================================
# File: util.py
# Auth: Andrew Calvano / Jim Ching
# Desc: General utility functions.
#
# Changelog
#	* Fixed getvin; randint(0,len(alphanumeric) - 1) otherwise index error.
#	* Added pydoc comment headers.
#==============================================================================
from os import urandom
from binascii import hexlify
from Crypto.Hash import SHA256
from string import digits, uppercase
from random import randint

# Subset of ASCII; digit and uppercase letters.
alphanumeric = digits + uppercase

def genvin():
	'Generate a 18 byte string of digits and capitalize letters.'
	return ''.join([alphanumeric[randint(0,len(alphanumeric) - 1)] for x in range(17)])

def getsalt():
	'Generate a 32 byte string based off a random 16 byte string.'
	return hexlify(urandom(16))

def createhash(salt, password):
	'Apply SHA256 on salt + password and return 128 byte string.' 
	thehash = SHA256.new(salt + password)
	return thehash.hexdigest()