from Crypto.Util.number import bytes_to_long
from random import getrandbits

m = getrandbits(48)
a = getrandbits(16)
b = 0
seed = getrandbits(48)

state = seed

def next_lcg():
    global state
    state = (a * state + b) % m
    return state

lcgs = [next_lcg() >> 40 for _ in range(16)]

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(flag)

num = 0
while num < flag:
    num = (num << 48) | next_lcg()

print(f"m = {m}")
print(f"a = {a}")
print(f"lcgs = {lcgs}")
print(f"cipher = {flag ^ num}")