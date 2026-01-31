from tqdm import tqdm
import sys
from Crypto.Util.number import long_to_bytes
import string

exec(open("output").read())

pub1, pub2 = pubKey[:len(pubKey)//2], pubKey[len(pubKey)//2:]

sumMap1 = {}
for mask in tqdm(range(1 << len(pub1))):
    s = 0
    for i in range(len(pub1)):
        if mask & (1 << i):
            s += pub1[i]
    sumMap1[s] = mask

msg_lst = [[] for _ in range(len(ct_lst))]
for mask in tqdm(range(1 << len(pub2))):
    s = 0
    for i in range(len(pub2)):
        if mask & (1 << i):
            s += pub2[i]
    remainSums = [ct - s for ct in ct_lst]
    for i, remains in enumerate(remainSums):
        if remains in sumMap1:
            mask1 = sumMap1[remains]
            mask2 = mask

            num = (mask2 << len(pub1)) + mask1
            msg = long_to_bytes(num)
            if all(chr(c) in string.printable for c in msg):
                msg_lst[i].append(msg)
                print(f"Found message: {msg}")
                print()
print(msg_lst)
