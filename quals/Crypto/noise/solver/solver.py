from PIL import Image
import numpy as np
import imageio
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from tqdm import tqdm
import itertools
import string

def decrypt(encFrames, password):
    try:
        frames = []
        for i, encFrame in enumerate(encFrames):
            key = PBKDF2(password[i], b'salt', dkLen=16, count=1000)
            cipher = AES.new(key, AES.MODE_ECB)
            data = bytes.fromhex(encFrame)
            decrypted = cipher.decrypt(data)
            frame_pixels = np.frombuffer(decrypted, dtype=np.uint8).reshape((height, width))        
            frames.append(frame_pixels)

        xor_result_np = np.bitwise_xor(frames[0], frames[1])
        xor_result_image = Image.fromarray(xor_result_np.astype(np.uint8))
        xor_result_image.save(f'solution/xor_result_{password}.png')
    except:
        return

exec(open("output").read())

i = 0
for password in range(0xff + 1):
    password = hex(password)[2:].zfill(2)
    print(f'Trying key: {password}')
    decrypt(enc[:2], password)
    i += 1