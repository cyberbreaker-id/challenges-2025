from Crypto.Util.number import bytes_to_long, long_to_bytes
import numpy as np

def secretFunction(x):
    return x**3 - 6*x**2 + 14*x - 4

decrypted = ['53b8cd6b', '1d07448b', '0c4cc503', 'a2b878f3', '9b891e90', '1ab44eaa', '7607119b', '9e876fff', '6fdee846', 'a092a76e', '2f980193', '9c914c11', '30a50adb', '6bf66877', '8b1b596d', '19bfbde6', '4e8260af', '2a1d0de4', '1d7c8272', '39d7f974', '47761e11', 'a8608689', '9c87e718', 'a2896471', '0a675a33', '6bf66877', '9a226ce5', '76c75656', '50de38e0', '6a013335', '445ce9c8', '6ca89d48', '31d63be0', '5ed72ce9', '0e7c229f', '25403c2d', '6069e075', '824a1eb8', '2cc01eca', '99fee92f', 'ab28498a', '7817ae05', '64021828', '239dd035']
key = [149, 197, 211, 191, 181, 131, 251, 197, 229, 199, 163, 137, 163, 251, 131, 149, 149, 223, 151, 191, 191, 227, 173, 241, 131, 251, 173, 151, 191, 233, 241, 241, 131, 137, 241, 163, 131, 191, 179, 157, 251, 137, 167, 239]
N = 2880782939

failedDecrypted = [int(c,16) for c in decrypted]

cipher = []
for fd, k in zip(failedDecrypted, key):
    c = fd * secretFunction(k) % N
    cipher.append(c)

knownPlaintext = 'CBC{'
x = []
y = []
for i in range(len(knownPlaintext)):
    nump = bytes_to_long(knownPlaintext[i].encode())
    fx = cipher[i] // nump
    x.append(key[i])
    y.append(fx)

coefficients = np.polyfit(x, y, 3)
secretFunction2 = np.poly1d(coefficients)

flag = b''
for c, k in zip(cipher, key):
    fx = round(secretFunction2(k))
    m = long_to_bytes((c * pow(fx, -1, N)) % N)
    flag += m
print(flag)