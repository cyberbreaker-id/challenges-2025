import binascii
from Crypto.Cipher import DES
from tqdm import tqdm
import itertools

exec(open("output.txt").read())
cipher = bytes.fromhex(cipher)

def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

known_plain = b"Here's your flag: CBC{"[:8]
known_cipher = cipher[:8]

first_key = {}
for key in tqdm(map("".join, itertools.product("0123456789", repeat=6)), total = 10**6):
    des = DES.new(pad(key), DES.MODE_ECB)
    enc = des.encrypt(known_plain)
    first_key[enc] = key

for key2 in tqdm(map("".join, itertools.product("0123456789", repeat=6)), total = 10**6):
    des2 = DES.new(pad(key2), DES.MODE_ECB)
    dec = des2.decrypt(known_cipher)
    if dec in first_key.keys():
        key1 = first_key[dec]
        des2 = DES.new(pad(key2), DES.MODE_ECB)
        des1 = DES.new(pad(key1), DES.MODE_ECB)
        msg = des1.decrypt(des2.decrypt(cipher))
        print(msg)
        break