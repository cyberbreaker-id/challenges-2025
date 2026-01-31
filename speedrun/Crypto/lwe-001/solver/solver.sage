from Crypto.Util.number import bytes_to_long
import random
import string
from itertools import product

def keygen():
    A = Matrix(3, 3, [random.randint(1, 256) for _ in range(9)])
    s = Matrix(3, 3, [random.randint(1, 256) for _ in range(9)])
    return A, s

def decodeChar(m):
    m_bits = "".join(str(x) for x in m.list())
    m_bits = m_bits[1:] + m_bits[0]
    if all(x in "01" for x in m_bits):
        return chr(int(m_bits, 2))
    else:
        raise ValueError("Decoding failed")

def decrypt(cipher, A, s, q=257):
    c = Matrix(3, 3, cipher)
    m = (c - A * s) % q
    for i in range(3):
        for j in range(3):
            m[i, j] = (m[i, j] > q//4 and m[i, j] < 3*q//4)
    return m

A = [14, 80, 62, 145, 183, 117, 173, 41, 157]
cipher = [[83, 15, 29, 167, 162, 142, 213, 28, 104], [213, 15, 30, 167, 163, 141, 214, 27, 102], [84, 14, 28, 165, 163, 141, 213, 28, 103], [83, 14, 30, 166, 34, 12, 85, 27, 103], [213, 13, 28, 165, 34, 141, 214, 29, 104], [83, 15, 29, 38, 35, 12, 212, 156, 103], [82, 13, 30, 167, 33, 141, 212, 157, 233], [212, 15, 30, 38, 33, 14, 213, 29, 233], [212, 15, 29, 39, 33, 14, 213, 157, 233], [83, 14, 29, 37, 33, 12, 214, 155, 104], [213, 15, 29, 166, 35, 143, 212, 157, 232], [213, 13, 29, 166, 35, 143, 213, 27, 104], [212, 13, 28, 37, 34, 14, 212, 157, 102], [83, 15, 28, 166, 34, 143, 214, 28, 102], [83, 14, 28, 167, 34, 141, 212, 157, 232], [211, 14, 30, 166, 34, 143, 214, 155, 232], [212, 15, 28, 38, 35, 13, 214, 155, 104], [83, 15, 28, 37, 35, 14, 214, 156, 232], [211, 14, 28, 166, 35, 142, 214, 27, 103], [83, 15, 28, 37, 34, 13, 213, 27, 231], [211, 14, 28, 167, 33, 141, 214, 155, 103], [82, 15, 28, 37, 33, 14, 213, 29, 104], [83, 13, 28, 167, 35, 141, 212, 29, 102], [84, 14, 30, 37, 35, 13, 213, 28, 233], [211, 14, 29, 165, 33, 142, 212, 156, 102], [213, 14, 29, 38, 34, 14, 213, 155, 233], [82, 13, 30, 167, 33, 143, 212, 156, 231], [82, 14, 28, 39, 34, 14, 213, 155, 232], [211, 13, 29, 165, 35, 142, 212, 157, 104], [212, 14, 29, 166, 35, 141, 214, 28, 103], [84, 15, 29, 166, 33, 142, 212, 157, 231], [213, 13, 28, 38, 34, 13, 213, 28, 103], [83, 15, 30, 37, 34, 14, 212, 157, 231], [213, 14, 30, 37, 33, 14, 213, 155, 231], [212, 14, 29, 37, 34, 13, 213, 156, 102], [83, 14, 28, 38, 35, 12, 213, 156, 104], [83, 14, 29, 167, 33, 14, 84, 157, 231]]

A = Matrix(3, 3, A)

# error on testprint() gives us matx * s + A * q//2 + e
# char '#' encoded as 100010001 or identity matrix
# thus, testprint('#') gives us I * s + A * q//2 + e
testPrint = Matrix(3, 3, [111, 139, 116, 215, 18, 90, 152, 142, 172]) # from testPrint('#')

# Generate all possible error for 9 variables, each in range(-1, 0, 1)
for vals in product(range(-1, 1), repeat=9):
    e = Matrix(3, 3, vals)
    s = (testPrint - A * (257 // 2) - e) % 257
    plain = ""
    for c in cipher:
        dec = decrypt(c, A, s)
        try:
            plain += decodeChar(dec)
        except ValueError:
            break
    if plain.startswith("CBC{") and plain.endswith("}"):
        print(f"Found! s = {s.list()}")
        print(f"Flag: {plain}")
        break

