import numpy as np

exec(open("output").read())
from Crypto.Util.number import long_to_bytes, bytes_to_long

s0 = bytes_to_long(b'The Flag')
s1 = bytes_to_long(b' is CBC{')

s = [s0, s1]
for i in range(len(enc1)):
    bc = np.bitwise_xor(enc1[i], np.bitwise_and(s[-1], s[-2])) #BC = ENC1 XOR AB
    not_bc = np.bitwise_xor(enc2[i], np.bitwise_and(np.bitwise_not(s[-1]), np.bitwise_not(s[-2]))) # ~B~C = ENC2 XOR ~A~B
    xnor_bc = np.bitwise_or(bc, not_bc) # B XNOR C = BC + ~B~C
    c = np.bitwise_not(np.bitwise_xor(xnor_bc, s[-1])) # C = ~(xnor_bc XOR B)
    s.append(int(c))
    
s = [long_to_bytes(x) for x in s]
print(b''.join(s))

    