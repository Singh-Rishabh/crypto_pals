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
		tmp_string = tmp_string + chr(block_size)
	return s+tmp_string


def xor(data, key): 
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(data, key)) 

def rand_AES_KEY(block_size):
	return urandom(block_size)

def encrypt_ecb(key,m):
	tmp = len(key)
	m = padding(tmp,m)
	cipher_text = ""
	ecb_obj = AES.new(key, AES.MODE_ECB)
	for i in range(0,len(m),tmp):
		substr = m[i:i+tmp]
		cipher_text = cipher_text + ecb_obj.encrypt(substr)	
	return cipher_text


def enc_oracle(m):
	cipher_text = encrypt_ecb(key,m)
	return cipher_text
	

def get_blocks(cipher_text, blocksize=16):
	x = [cipher_text[i:i+blocksize] for i in range(0, len(cipher_text), blocksize)]	
	return x


def detect_block_size():
	# global postfix 
	# print (postfix)
	plaintext = 'A' + postfix
	cipher_text1 = enc_oracle(plaintext)
	for i in range(40):
		plaintext = 'A' + plaintext
		cipher_text = enc_oracle(plaintext)
		if cipher_text1 in cipher_text:
			blocksize = i+1
			# print(blocksize)
			break
	return blocksize

def create_dict(blocksize):
	dict_1_block_cipher = {}
	for i in range(256):
		plaintext = 'A'*(blocksize - 1) + chr(i)
		dict_1_block_cipher[enc_oracle(plaintext)] = plaintext
	# print dict_1_block_cipher
	# print dict_1_block_cipher['A'*(blocksize - 1) + chr(97)]
	# print('A'*(blocksize - 1) + chr(97))
	return dict_1_block_cipher

def decrypt_text(blocksize,dict_1_block_cipher):
	unknown_String = ""
	for i in range(len(postfix)):
		plaintext = 'A'*(blocksize - 1) + postfix[i]
		cipher_text = enc_oracle(plaintext)
		unknown_String = unknown_String +  dict_1_block_cipher[cipher_text][-1]
	# print(len(unknown_String))
	return unknown_String

	

block_size = 16
key = rand_AES_KEY(block_size)



postfix = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'''
postfix = postfix.decode('base64')
blocksize = detect_block_size()
dict_1_block_cipher = create_dict(blocksize)
print decrypt_text(blocksize,dict_1_block_cipher)