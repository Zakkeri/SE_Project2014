#==============================================================================
# File: util.py
# Auth: Andrew Calvano / Jim Ching
# Desc: General utility functions.
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

def editdistance(s1, s2):
   'Edit distance algorithm: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python'
   if len(s1) < len(s2):
      return editdistance(s2, s1)
 
   # len(s1) >= len(s2)
   if len(s2) == 0:
      return len(s1)
 
   previous_row = range(len(s2) + 1)
   for i, c1 in enumerate(s1):
      current_row = [i + 1]
      for j, c2 in enumerate(s2):
         insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
         deletions = current_row[j] + 1       # than s2
         substitutions = previous_row[j] + (c1 != c2)
         current_row.append(min(insertions, deletions, substitutions))
      previous_row = current_row
 
   return previous_row[-1]

def validate_table(table, source):
   valid = True
   for entry in table:
      if entry not in source:
         valid = False; break
   return valid