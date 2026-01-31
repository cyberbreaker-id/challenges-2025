from Crypto.Util.number import long_to_bytes, bytes_to_long
import numpy as np
import random

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def encrypt(a, b, c):
    enc = np.bitwise_xor(np.bitwise_and(a, b), np.bitwise_and(b, c))
    return int(enc)

flag = b"The Flag is CBC{#REDACTED}"
flag  = chunks(flag, 8)
s = [bytes_to_long(x) for x in flag]

enc1 = []
enc2 = []
for i in range(2, len(s)):
    enc1.append(encrypt(s[i-2], s[i-1], s[i]))
    enc2.append(encrypt(np.bitwise_not(s[i-2]), np.bitwise_not(s[i-1]), np.bitwise_not(s[i])))

print("enc1 =", enc1)
print("enc2 =", enc2)