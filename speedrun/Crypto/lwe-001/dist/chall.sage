from Crypto.Util.number import bytes_to_long
import random
import string

def keygen():
    A = Matrix(3, 3, [random.randint(1, 256) for _ in range(9)])
    s = Matrix(3, 3, [random.randint(1, 256) for _ in range(9)])
    return A, s

def encodeChar(c):
    numc = bin(ord(c))[2:].zfill(9)
    numc = numc[-1] + numc[:-1]
    return Matrix(3, 3, map(int, numc))

def encrypt(plain, A, s, q=257):
    e = Matrix(3, 3, [random.randint(-1, 1) for _ in range(9)])
    enc = (A * s + plain * (q // 2) + e) % q
    return enc

def testPrint(A, s, q=257):
    print("--- Test Encrypt ---")
    plain = string.printable
    for x in plain:
        matx = encodeChar(x)
        enc = encrypt(A, matx, s, q)
        print(f"{x} -> {matx.list()} -> {enc.list()}")

A, s = keygen()

flag = open("flag.txt", "r").read().strip()
assert flag[:4] == "CBC{"

cipher = []
for plain in flag:
    matx = encodeChar(plain)
    cipher.append(encrypt(matx, A, s).list())

print(f"A = {A.list()}")
print(f"cipher = {cipher}")

testPrint(A, s)


