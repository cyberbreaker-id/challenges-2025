import random
from Crypto.Util.number import bytes_to_long

class myFunction:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def f(self, x):
        return (self.a * x * x + self.b * x + self.c)

    def encrypt(self, plaintext):
        ciphertext = []
        for i, char in enumerate(plaintext):
            key = self.f(i)
            ciphertext.append(char * key)
        return ciphertext

a = random.randint(1, 2**16)
b = random.randint(1, 2**16)
c = random.randint(1, 2**16)

func = myFunction(a, b, c)

flag = open("flag.txt", "rb").read()
cipher = func.encrypt(flag)

print(f"cipher = {cipher}")