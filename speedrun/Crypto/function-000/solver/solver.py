exec(open("output").read())

from Crypto.Util.number import bytes_to_long, long_to_bytes
import numpy as np

knownPlaintext = b'CBC{'
x = [i for i in range(len(knownPlaintext))]
y = [cipher[i]//knownPlaintext[i] for i in range(len(knownPlaintext))]

coefficients = np.polyfit(x, y, 2)
function = np.poly1d(coefficients)

flag = b""
for i in range(len(cipher)):
    c = cipher[i] // round(function(i))
    flag += bytes([c])

print(flag)