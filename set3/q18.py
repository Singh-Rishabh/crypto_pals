from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy
from os import urandom
from random import randint
from struct import *
 

def xor(data, key): 
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(data, key))

def encrypt_ecb(key,m):
	tmp = len(key)
	m = padding(tmp,m)
	cipher_text = ""
	ecb_obj = AES.new(key, AES.MODE_ECB)
	for i in range(0,len(m),tmp):
		substr = m[i:i+tmp]
		cipher_text = cipher_text + ecb_obj.encrypt(substr)	
	return cipher_text

def decrypt_ctr(ciphertext,nonce = 0):
	
	nonce = 0
	counter = 0
	iv = pack('<q',nonce) + pack('<q',counter) 
	keystream = b''
	while (len(keystream) < len(ciphertext)):
		ecb_obj = AES.new(key, AES.MODE_ECB)
		iv_cipher = ecb_obj.encrypt(iv)
		counter += 1
		iv = pack('<q',nonce) + pack('<q',counter) 
		keystream += iv_cipher

	if len(keystream) > len(ciphertext):
		keystream = keystream[:len(ciphertext)]

	plaintext = xor(ciphertext, keystream)
	return(plaintext)
	
key = "YELLOW SUBMARINE"
s = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
s = s.decode('base64')
print (decrypt_ctr(s))

