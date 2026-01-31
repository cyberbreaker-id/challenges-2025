from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, isPrime, inverse

def genKey(p, q):
    r = int(str(p) + str(q))
    s = int(str(q) + str(p))
    t = int(str(r) + str(s))
    u = int(str(s) + str(r))
    return t * u, t, u
    
exec(open('output').read())

lens = 39
high_pq = str(N)[:lens//2 - 1]
low_pq = str(N)[-lens//2 + 1:]

for i in range(100):
    str_i = f"{i:02d}"
    str_pq = high_pq + str_i + low_pq
    factors = factor(int(str_pq))
    primes = [int(f[0]) for f in factors]
    if len(primes) == 2:
        p, q = primes
        N_res, t, u = genKey(p, q)
        if N_res == N:
            phi = (t - 1) * (u - 1)
            m = pow(c, inverse(e, phi), N)
            print(long_to_bytes(m))
            break
        
