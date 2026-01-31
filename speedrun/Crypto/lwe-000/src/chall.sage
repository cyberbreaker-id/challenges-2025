from Crypto.Util.number import bytes_to_long
import random

while True:
    A = Matrix([[random.randint(1, 256) for _ in range(3)] for _ in range(3)])
    if A.is_invertible():
        break
        
key = [random.randint(1, 256) for _ in range(9)]
s = Matrix(3, 3, key)
e = Matrix(3, 3, [random.randint(-1, 1) for _ in range(9)])
q = 257

flag = open("flag.txt", "r").read().strip()
assert flag[:4] == "CBC{"

cipher = []
for i, plain in enumerate(flag):
    plain = Matrix(3, 3, map(int, f"{ord(plain):09b}"))
    enc = (A * s * (key[i % 9]) + plain * (q // 2) + e) % q
    cipher.append(enc.list())

print(f"A = {A.list()}")
print(f"cipher = {cipher}")