from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import random
key = os.urandom(16)

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    return cipher.encrypt(msg).hex()

flag = open("flag.txt", "rb").read()
txt = open("hamlet soliloquy.txt", "rb").read().splitlines()

enc = [encrypt(flag)]
for line in txt:
    enc.append(encrypt(line))
random.shuffle(enc)

print("enc =", enc)
