# from hashlib import md5
# from base64 import b64decode
# from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy

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


def encrypt_ecb(key,m):
	ecb_obj = AES.new(key, AES.MODE_ECB)
	cipher_text = ecb_obj.decrypt(m)
	return cipher_text


def decrypt_cbc(cipher_text,key,iv):
	aes_obj = AES.new('YELLOW SUBMARINE', AES.MODE_CBC, iv)
	plain_text = aes_obj.decrypt(cipher_text)
	return plain_text


# def encrypt(iv,m, key):
# 	tmp = len(iv)
# 	m = padding(tmp,m)
# 	cipher_text = ""
# 	for i in range(0,len(m),tmp):
# 		substr = m[i:i+tmp]
# 		if (len(substr) != tmp):
# 			print("Wrong Block")
		
# 		xor_m = xor(substr,iv)
# 		# print(xor(substr,iv))
# 		iv = encrypt_ecb(key,xor_m)
# 		cipher_text = cipher_text + iv

# 		if (len(xor(substr,iv)) != tmp):
# 			print("Wrong Blockdddddddddddddd")
# 	return cipher_text

def decrypt(iv,ct, key):
	tmp = len(iv)
	plain_text = ""
	for i in range(0,len(ct),tmp):
		substr = deepcopy(ct[i:i+tmp])
		temp = encrypt_ecb(key,substr)
		xor_m = xor(temp,iv)
		iv = deepcopy(substr)		
		plain_text = plain_text + xor_m

	return plain_text

	

f = open('q10.txt')
s = f.read().replace("\n", "")
f.close()
s = s.decode('base64')

print(s)
print("\n\n")

key = "YELLOW SUBMARINE"
iv = "0000000000000000"
aes_obj = AES.new('YELLOW SUBMARINE', AES.MODE_CBC , iv)
plain_text = aes_obj.decrypt(s)
print plain_text
print("\n**** my function \n")
print decrypt(iv,s,key)
