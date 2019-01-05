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
	m = random_prefix + m + target_message
	cipher_text = encrypt_ecb(key,m)
	return cipher_text
	

def get_blocks(cipher_text, blocksize=16):
	x = [cipher_text[i:i+blocksize] for i in range(0, len(cipher_text), blocksize)]	
	return x


def detect_random_prefix_size():
	plaintext = ""
	cipher_text0 = enc_oracle(plaintext)
	blocks0 = get_blocks(cipher_text0,block_size)
	blocks1 = []
	blocks2 = []
	len_block1 = 99999999999
	for i in range(1000):
		plaintext = 'A' + plaintext
		cipher_text = enc_oracle(plaintext)
		blocks = get_blocks(cipher_text,block_size)
		if (len(blocks) == len(blocks0) + 1):
			blocks1 = deepcopy(blocks)
			len_block1 = len(blocks1)
		# set_ct.add(cipher_text)

		if (len_block1 + 1 == len(blocks)):
			blocks2 = deepcopy(blocks)
			break
	index = -1

	for i in range(len_block1):
		if (blocks1[i] != blocks2[i]):
			index = i
			break

	plaintext = 'A'*16*2
	index2 = -1
	for i in range(33):
		cipher_text = enc_oracle(plaintext)
		if (len(get_blocks(cipher_text)) != len(set(get_blocks(cipher_text)))):
			index2 = i
			break
		plaintext = 'A' + plaintext

	padding = index2

	unknown_size = len(cipher_text) - index*blocksize - 32
	if ((index*blocksize - padding )%16 == 0):
		unknown_size = len(cipher_text) - index*blocksize 
		# return (index*blocksize - padding -16 , unknown_size)
	
	# print padding
	return (index*blocksize - padding , unknown_size)

# def create_dict(plaintext,blocksize):
# 	dict_1_block_cipher = {}
# 	for i in range(256):
# 		plaintext = plaintext + chr(i)
# 		dict_1_block_cipher[enc_oracle(plaintext)] = plaintext
# 	return dict_1_block_cipher


	

block_size = 16
key = rand_AES_KEY(block_size)

random_prefix_size = randint(20,100)
print random_prefix_size
random_prefix = urandom(random_prefix_size)

target_message = "Rishabh Singh Aditya tiwari - lodu  \Akaye - golu555555555"


blocksize = 16
(prefix_size ,unknown_size)= detect_random_prefix_size()
print(prefix_size , unknown_size , len(target_message))


num_blocks = unknown_size/blocksize
unknown_string = ""
extra = blocksize - prefix_size%blocksize
skip = prefix_size + extra
for num in range(num_blocks):
    str1 = "A"*(extra+blocksize-1)
    for i in range(blocksize):
        test1 = enc_oracle(str1)
        matching = dict()
        for j in range(255):
            str2 = str1 + unknown_string + chr(j)
            matching[enc_oracle(str2)[skip+num*blocksize:skip+num*blocksize+blocksize]] = str2
          
        tmp1 = test1[skip+num*blocksize:skip+num*blocksize+blocksize]
        tmp2 = matching[tmp1]
        new_byte = tmp2[-1]
        unknown_string=unknown_string+new_byte
        str1 = str1[1:]
print unknown_string