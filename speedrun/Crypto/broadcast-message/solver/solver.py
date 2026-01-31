from Crypto.Util.number import bytes_to_long, long_to_bytes
from egcd import egcd

exec(open('output').read())

gcd, a, b = egcd(e1, e2)
assert gcd == 1, "e1 and e2 are coprime"

m = pow(c1, a, N) * pow(c2, b, N) % N

print(long_to_bytes(m))