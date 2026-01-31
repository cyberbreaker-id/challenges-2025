# Implementation of Affine Cipher in Python
import random

chrMap  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{_}"

def affine_encrypt(text, key):
    cipher = ""
    for c in text:
        cipher += chrMap[(key[0] * (chrMap.index(c)) + key[1]) % len(chrMap)]
    return cipher

text = open("flag.txt", "r").read().strip()
key = [random.getrandbits(64), random.getrandbits(64)]
cipher = affine_encrypt(text, key)
print(f"cipher = '{cipher}'")