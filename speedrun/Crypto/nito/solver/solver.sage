from Crypto.Util.number import long_to_bytes
load("coppersmith.sage")

exec(open("../dist/output.txt").read())

nbits = 256
kbits = 64
K = 1 << kbits

P.<x,y> = PolynomialRing(GF(p))
delta = 1 / 4
bounds = (floor(p^delta), floor(p^delta))
f = (y + b1 * K) - ((x + b0 * K)^2)
roots = small_roots(f, bounds)

x0, y0 = roots[0]
a0, a1 = x0 + b0 * K, y0 + b1 * K

m = c ^^ pow(int(a1), 42, p)
flag = long_to_bytes(m)

print(flag)
