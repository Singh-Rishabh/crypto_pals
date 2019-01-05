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

def encrypt_cbc(key,m,iv):
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


def enc_oracle(m,iv_len):
	key = rand_AES_KEY(iv_len)
	iv = urandom(iv_len)
	prefix = randint(5, 10)
	suffix = randint(5, 10)
	plaintext = urandom(prefix) + m + urandom(suffix)
	encrypt_type = randint(0,1)
	if (encrypt_type == 0) :
		cipher_text = encrypt_ecb(key,m)
	else:
		cipher_text = encrypt_cbc(key,m,iv)

	if (encrypt_type == 0):
		encrypt_type = 'ECB'
	else :
		encrypt_type = 'CBC'
	return (cipher_text,encrypt_type)

def get_blocks(cipher_text, blocksize=16):
	x = [cipher_text[i:i+blocksize] for i in range(0, len(cipher_text), blocksize)]	
	return x

def detect_cipher_mode(iv_len):
	m = ""
	for i in range(100):
		m = m + 'a'

	(cipher_text,ans) = enc_oracle(m,iv_len)
	num_blocks = len(get_blocks(cipher_text,iv_len))
	num_unique_blocks = len(set(get_blocks(cipher_text,iv_len)) )

	if (num_unique_blocks < num_blocks):
		return ("Adversory: ECB, actual: " + ans) 
	else:
		return ("Adversory: CBC, actual: " + ans)

iv_len = 16



print(detect_cipher_mode(iv_len))
print(detect_cipher_mode(iv_len))
print(detect_cipher_mode(iv_len))
print(detect_cipher_mode(iv_len))


