exec(open("output").read())

import random 
from Crypto.Util.number import long_to_bytes

print(factor(fc)) #find factor fc that has 64 bits
c = 16792313112762132853
print(factor(fb - c)) #find factor of fb - c that has 64 bits
b = 10272508761957936139
print(factor(fa - c)) #find factor of fa - c that has 64 bits
a = 11264287525071499069

assert fa == a * a * a + b * a + c
seed = solve(a * x * x + b * x + c == f_seed, x)[1].rhs()
random.seed(int(seed))

key = random.randint(1, 2 ** 128)
f_key = a * key * key + b * key + c
flag = f_key.__xor__(cipher)
print(long_to_bytes(flag))