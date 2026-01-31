from Crypto.Util.number import bytes_to_long

flag = b"CBC{******** redacted ********}"

nbits = 256
kbits = 64

p = random_prime(1 << nbits)
a0 = randrange(p)
a1 = pow(a0, 2, p)
b0, b1 = a0 >> kbits, a1 >> kbits

c = bytes_to_long(flag) ^^ pow(a1, 42, p)

print(f"{p=}")
print(f"{c=}")
print(f"{b0=}")
print(f"{b1=}")
