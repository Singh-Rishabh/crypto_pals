from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy
from os import urandom
from random import randint


key = urandom(16)

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


def fun_1(m):
	prefix = 'comment1=cooking%20MCs;userdata='
	suffix = ';comment2=%20like%20a%20pound%20of%20bacon'
	m = m.replace('=','').replace(';','').replace('%','')
	m = prefix + m + suffix
	cipher_text = encrypt_cbc(key,m)
	return cipher_text

