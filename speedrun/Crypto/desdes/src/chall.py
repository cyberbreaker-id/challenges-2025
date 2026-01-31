#!/usr/bin/python3 -u
from Crypto.Cipher import DES
import binascii
import itertools
import random
import string

def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

def encrypt(m, key):
    des1 = DES.new(pad(key[:6]), DES.MODE_ECB)
    des2 = DES.new(pad(key[-6:]), DES.MODE_ECB)
    
    cipher = des2.encrypt(des1.encrypt(pad(m)))
    return binascii.hexlify(cipher).decode()

key = "".join(random.choice(string.digits) for _ in range(16))

flag = "Here's your flag: CBC{14300a868d7805ae1b6e9b16c953d931}"
cipher = encrypt(flag, key)

print(f"cipher = '{cipher}'")