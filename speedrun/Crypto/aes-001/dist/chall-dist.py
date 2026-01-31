from Crypto.Cipher import AES
import os
import random


key = os.urandom(16)
message = b'The flag is CBC{#REDACTED} Can you find it?'

enc = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
cipher = enc.encrypt(message)

print(f"key = '{key[:13].hex()}'")
print(f"cipher = '{cipher.hex()}'")