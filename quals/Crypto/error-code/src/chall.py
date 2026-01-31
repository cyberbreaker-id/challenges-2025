import random
from collections import namedtuple
import gmpy2
from Crypto.Util.number import isPrime, bytes_to_long, inverse, long_to_bytes

flag = open('flag.txt', 'rb').read()
PrivateKey = namedtuple("PrivateKey", ['W', 'q', 'r'])

def getSequence(size):
    W = []
    w0 = 99999
    for _ in range(size):
        wi = random.randint(w0 + 1, 2 * w0)
        W.append(wi)
        w0 = wi
    return W

def genPrivateKey(size):
    W = getSequence(size)
    while True:
        q = random.randint(2 * sum(W), 32 * sum(W))
        if isPrime(q):
            break
    while True:
        r = random.randint(sum(W), q)
        if gmpy2.gcd(q, r) == 1:
            break
    assert q > sum(W)
    return PrivateKey(W, q, r)

def genPublicKey(privKey: PrivateKey):
    pubKey = [(privKey.r * wi) % privKey.q for wi in privKey.W]
    return pubKey

def encrypt(pubKey, msg):
    ct_lst = []
    msg = bytes_to_long(msg)
    while msg:
        ct = 0
        for bi in pubKey:
            ct += (msg & 1) * bi
            msg >>= 1
        ct_lst.append(ct)
    return ct_lst

size = len(flag)
privKey = genPrivateKey(size)
pubKey = genPublicKey(privKey)
ct_lst = encrypt(pubKey, flag)

print(f'pubKey = ',pubKey)
print(f'ct_lst = ', ct_lst)