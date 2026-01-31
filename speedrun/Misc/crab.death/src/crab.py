import os

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

m1 = b"here is your flag CBC{REDACTED}"
m2 = b"meet me at the old bridge before sunset"

key = os.urandom(max(len(m1), len(m2)))

c1 = xor(m1, key[:len(m1)])
c2 = xor(m2, key[:len(m2)])

print("C1 =", c1.hex())
print("C2 =", c2.hex())
