from os import urandom
from Crypto.Util.number import long_to_bytes

# https://gist.github.com/maple3142/c7c31d2e5893d524e71eb5e12b0278f0#file-truncated_lcg-py

def get_L(k):
    M = matrix([m])
    A = matrix([a ** i for i in range(1, k)]).T
    I = matrix.identity(k - 1) * -1
    Z = matrix([0] * (k - 1))
    L = block_matrix([[M, Z], [A, I]])
    return L


def solve_tlcg(ys, s=2 ** 40):
    # Solve x_{n+1}=a*x_n (mod m) given multiple top bits of x_n
    # https://crypto.stackexchange.com/questions/37836/problem-with-lll-reduction-on-truncated-lcg-schemes
    k = len(ys)
    L = get_L(k)
    B = L.LLL()
    sys = vector(y * s for y in ys)
    sby = B * sys
    ks = vector(round(x) for x in sby / m)
    zs = B.solve_right(ks * m - sby)
    return list(sys + zs)

exec(open("output.txt").read())
next_val = solve_tlcg(lcgs)[-1]

num = 0
while True:
    next_val = next_val * a % m
    num = (num << 48) | (next_val)
    
    plain = num.__xor__(cipher)
    flag = long_to_bytes(plain)
    if flag.startswith(b"CBC{"):
        print(f"Flag: {flag}")
        break