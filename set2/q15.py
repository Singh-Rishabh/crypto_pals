from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy
from os import urandom
from random import randint

def check_valid_padding(plaintext):
	tmp = plaintext[-1]
	# print tmp
	# print (ord(tmp))

	for i in range(ord(tmp)):
		# print (plaintext[-i-1])
		if (plaintext[-i - 1] != tmp):
			return False
	return True

print (check_valid_padding("ICE ICE BABY\x04\x04\x04\x04"))
print (check_valid_padding("ICE ICE BABY\x05\x05\x05\x05"))