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

def decrypt_ecb(cipher_text):

    tmp = len(key)
    plain_text = ""
    ecb_obj = AES.new(key, AES.MODE_ECB)
    for i in range(0,len(cipher_text),tmp):
        substr = cipher_text[i:i+tmp]
        plain_text = plain_text + ecb_obj.decrypt(substr) 
    return plain_text

def profile_creation(email_id):
    email_id = email_id.replace('&','').replace('=','')
    profile = {}
    profile['email'] = email_id
    profile['uid'] = 10
    profile['role'] = 'user'
    output = ''
    output = 'email=' + email_id + '&uid=' + str(10) + '&role=user'
    return output
    


def make_admin_profile():
    enc_admin = enc_oracle('admin')
    enc_user = enc_oracle(profile_creation('foo@gmail.com'))
    mod_enc = enc_user[0:len(enc_user)-16] + enc_admin
    return mod_enc

key = urandom(16)
b = profile_creation('foo@gmail.com')
enc = enc_oracle(b)
mod_enc = make_admin_profile()
print(decrypt_ecb(mod_enc))

