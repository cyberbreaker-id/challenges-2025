from Crypto.Util.number import long_to_bytes, bytes_to_long
import numpy as np
import random

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def encrypt(a, b, c):
    eq1 = np.bitwise_and(b, c)
    eq2 = np.bitwise_and(a, np.bitwise_not(b))
    eq3 = np.bitwise_not(np.bitwise_or(a, eq1))
    eq4 = np.bitwise_not(eq2)
    return int(np.bitwise_not(np.bitwise_or(eq3, eq4)))

flag = open("flag.txt", "rb").read()
flag  = chunks(flag, 7)
s = [bytes_to_long(x) for x in flag]

m0 = random.getrandbits(7*8)
m1 = random.getrandbits(7*8)

enc = []
enc.append(encrypt(m0, s[0], m1))
enc.append(encrypt(s[0], m0, m1))

for i in range(1, len(s)):
    enc.append(encrypt(s[i], s[i-1], m0))
    enc.append(encrypt(s[i-1], s[i], m1))

print("m0 =", m0)
print("enc =", enc)