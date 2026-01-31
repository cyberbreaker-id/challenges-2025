from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime

def genKey():
    p = getPrime(512)
    q = getPrime(512)
    return p * q

flag = open("flag.txt", "rb").read().strip()

N = genKey()
e1 = 65537
e2 = 61543
e3 = 56383

c1 = pow(bytes_to_long(flag), e1, N)
c2 = pow(bytes_to_long(flag), e2, N)
c3 = pow(bytes_to_long(flag), e3, N)

print(f"c1 = {c1}")
print(f"c2 = {c2}")
print(f"c3 = {c3}")

print(f"e1 = {e1}")
print(f"e2 = {e2}")
print(f"e3 = {e3}")

print(f"N = {N}")
