import numpy as np

exec(open("output").read())
from Crypto.Util.number import long_to_bytes, bytes_to_long

def decrypt(eq1, eq2, A):
    eq = np.bitwise_xor(np.bitwise_or(eq1, eq2), A)
    return int(eq)

s = [decrypt(enc[0], enc[1], m0)]
for i in range(1, len(enc)//2):
    s.append(decrypt(enc[2*i], enc[2*i+1], s[-1]))
s = [long_to_bytes(x) for x in s]

print(b''.join(s))