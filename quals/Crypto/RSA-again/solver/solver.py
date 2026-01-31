from sympy import nextprime, isprime
from Crypto.Util.number import bytes_to_long, getPrime, inverse, long_to_bytes

exec(open('output').read())

def genQ(p):
    return nextprime((p << 128))

def binarySearch(N, maxP):
    low = 2
    high = maxP
    while low <= high:
        p = low + (high - low) // 2
        print(p)
        q = genQ(p)

        if N % p == 0:
            return p
        elif p * q < N:
            low = p + 1
        else:
            high = p - 1
    return -1

p = binarySearch(n, 1 << 1024 + 1)
assert n % p == 0
q = n // p
d = inverse(e, (p - 1) * (q - 1))
m = pow(c, d, n)
flag = long_to_bytes(m)
print(flag)