from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.number import getPrime
import random

def secretFunction2(x):
    return 2*x**3 - 12*x**2 + 256*x - 10

def secretFunction(x):
    return x**3 - 6*x**2 + 14*x - 4

def encrypt(message, key, N):
    cipher = []
    for m, k in zip(message, key):
        c = bytes_to_long(m.encode()) * secretFunction2(k) % N
        cipher.append(c)
    return cipher

def decrypt(ciphertext, key, N):
    message = []
    for c, k in zip(ciphertext, key):
        m = long_to_bytes((c * pow(secretFunction(k), -1, N)) % N)
        message.append(m.hex())
    return message
  
message = "CBC{O0Pps_0ur_FunCt1oN_iS_n0t_th3_s4m3_H4h4}"
key = [getPrime(8) for _ in range(len(message))]
N = 2880782939

encrypted_message = encrypt(message, key, N)

decrypted_message = decrypt(encrypted_message, key, N)

print("decrypted =", decrypted_message)
print("key =", key)
print("N =", N)