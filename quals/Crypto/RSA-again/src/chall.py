from sympy import nextprime, isprime
from Crypto.Util.number import bytes_to_long, getPrime

def genKey():
    p = getPrime(1024)
    q = nextprime((p << 128))
    return p, q

flag = open('flag.txt', 'rb').read()
p, q = genKey()
n = p * q
e = 65537 
c = pow(bytes_to_long(flag), e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')