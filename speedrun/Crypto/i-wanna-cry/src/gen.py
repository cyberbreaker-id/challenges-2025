#!/usr/bin/env python3
import math
from Crypto.PublicKey import RSA
from secret import FLAG, E

bits = 1024
count = 3
output_file = "output.txt"

m = int.from_bytes(FLAG, "big")

while True:
    keys = [RSA.generate(bits, e=E) for _ in range(count)]
    if m**E < math.prod([k.n for k in keys]):
        break

ns = [k.n for k in keys]
cs = [pow(m, E, n) for n in ns]

with open(output_file, "w") as f:
    for i, (n, c) in enumerate(zip(ns, cs), 1):
        f.write(f"N{i} = {n}\n")
        f.write(f"c{i} = {c}\n\n")

print(f"Challenge written to {output_file}")
