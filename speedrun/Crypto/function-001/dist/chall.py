import random
from Crypto.Util.number import bytes_to_long, getPrime

class myFunction:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def f(self, x):
        return (self.a * x * x + self.b * x + self.c)

    def encrypt(self, plaintext):
        key = random.randint(1, 2 ** 128)
        return plaintext ^ self.f(key)
    
seed = random.randint(1, 2**128)
random.seed(seed)

a = getPrime(64)
b = getPrime(64)
c = getPrime(64)
func = myFunction(a, b, c)

f_seed = func.f(seed)
flag = open("flag.txt", "rb").read()
flag = bytes_to_long(flag)
cipher = func.encrypt(flag)

print(f"fa = {func.f(a)}")
print(f"fb = {func.f(b)}")
print(f"fc = {func.f(c)}")
print(f"f_seed = {f_seed}")
print(f"cipher = {cipher}")