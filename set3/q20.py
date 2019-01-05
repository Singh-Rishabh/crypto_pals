from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from copy import deepcopy
from os import urandom
from random import randint
from struct import *

prob_char = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

def xor(data, key): 
    return ''.join(chr(ord(a)^ord(b)) for a, b in zip(data, key))


def get_val(k):
    val=0
    for i in k:
        if i in prob_char:
            val += prob_char[chr(i)]
    return val      

def get_key(ct):
    key = ''
    for i in range(len(ct[0])):
        print i
        max_ = -1
        arr = [x[i] for x in ct]
        x = ""
        for j in arr:
            x += j
        tmp = ''
        for j in range(0,256):
            chr_str = ''
            for k in range(len(x)):
                chr_str += chr(j)
            temp = xor(x,chr_str)
            print temp , j
            tmpval = get_val(temp)
            if (tmpval > max_):
                max_ = tmpval
                tmp = chr(j)
        key += tmp
    return key  

def decrypt_ctr(ciphertext,nonce = 0):
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
    


key = urandom(16)
line = ""
min_len_ = 999999
file_ = open('q20.txt')

for line in file_:
    if(len(line.decode('base64'))< min_len_):
        min_len_ = len(line.decode('base64'))
file_.close()
file_ = open('q20.txt')
plaintext = []
for line in file_:
    plaintext.append(line.decode('base64')[0:min_len_])
    # print (len(line.decode('base64')[0:min_len_]))

ct = []

for ct_ in plaintext:
    ct.append(decrypt_ctr(ct_))

# print ct
key = get_key(ct)
print(key)
