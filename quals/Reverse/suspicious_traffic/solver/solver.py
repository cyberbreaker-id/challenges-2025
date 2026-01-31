import os
from wincrypto import CryptCreateHash, CryptHashData, CryptDeriveKey, CryptEncrypt, CryptDecrypt, CryptImportKey, CryptExportKey
from wincrypto.constants import *
from Crypto.Util.number import *
import json
import string
import hashlib

dict_user = {}
dict_sha_256 = {}

for i in string.printable[:-6]:
	dict_sha_256[hashlib.sha256(i.encode()).hexdigest()] = i

def lcg(x, a, c, m):
    while True:
        x = (a * x + c) % m
        x &= 2**32 - 1
        yield x

LCG_M = 10187327
LCG_A = 12125293
LCG_C = 11999789
SEED = 12330767 # healthcheck

def decrypt(func_lcg, ct):
    hasher = CryptCreateHash(CALG_MD5)
    key = generate_key(func_lcg)
    CryptHashData(hasher, key)
    aes_key = CryptDeriveKey(hasher, CALG_AES_256)
    pt = CryptDecrypt(aes_key, ct)
    return pt

def generate_key(func_lcg):
    list_chr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = ''
    for i in range(16):
        key += list_chr[(next(func_lcg) * 1337) % len(list_chr)]
    return key.encode()


func_lcg = lcg(SEED, LCG_A, LCG_C, LCG_M)

f = open("dump.json", "r").read() # filter wireshark http and dump as json
data = json.loads(f)

list_pt = []

for i in range(len(data)):
	layer = data[i]["_source"]["layers"]
	if "json" in layer:
		tmp = json.loads(layer["json"]["json.object"])
		if "payload" in tmp:
			payload = tmp["payload"]
			list_pt.append(decrypt(func_lcg, bytes.fromhex(payload)))

flag = [0 for _ in range(42)]

for i in range(len(list_pt)):
	if b"powershell" in list_pt[i]:
		index = int(list_pt[i].decode().split(")[")[-1].split("]")[0])
		flag[index] = dict_sha_256[list_pt[i+1].strip().lower().decode()]
print(''.join(flag))


