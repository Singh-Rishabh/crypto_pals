from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy
from os import urandom
from random import randint


def padding(block_size,s):
	tmp = len(s)%block_size
	if (tmp == 0):
		tmp = block_size
	else:
		tmp = block_size - tmp
	tmp_string = ""
	for i in range(tmp):
		tmp_string = tmp_string + chr(tmp)
	return s+tmp_string

def xor(data, key): 
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(data, key))

def encrypt_cbc(key,m,iv = b'\x00'*16):
	tmp = len(iv)
	m = padding(tmp,m)
	cipher_text = ""
	cbc_obj = AES.new(key, AES.MODE_ECB)
	for i in range(0,len(m),tmp):
		substr = m[i:i+tmp]
		xor_m = xor(substr,iv)
		iv = cbc_obj.encrypt(xor_m)
		cipher_text = cipher_text + iv	
	return cipher_text


def enc_oracle(m):
	cipher_text = encrypt_cbc(key,m)
	return cipher_text
	

def dec_oracle(ciphertext, iv=b'\x00'*16):
	obj = AES.new( key , AES.MODE_CBC,iv )
	plaintext = obj.decrypt(ciphertext)
	return plaintext
	
def check_padding(plaintext):
	last = ord(plaintext[-1])
	# print(last)
	for i in range(last):
		if ord(plaintext[-i-1]) != last:
			return False
	return True
	
key = urandom(16)
block_size = 16

plain_text_arr = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=" , 
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=" , 
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==" ,
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93" ]

rand_index = randint(0, 9)
plaintext = plain_text_arr[rand_index].decode('base64')
print(plaintext)
ciphertext = enc_oracle(plaintext)
# print(ciphertext)
plaintext1 = dec_oracle(ciphertext)
print(ord(plaintext1[len(plaintext1)-1]))
print(len(plaintext1), len(plaintext))
print(check_padding(plaintext1))

	
