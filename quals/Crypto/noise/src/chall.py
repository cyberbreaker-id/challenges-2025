from PIL import Image
import numpy as np
import imageio
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(image, password):
    arr = []
    for y in range(height):
        tmp = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            tmp.append(int(pixel < 200))
        arr.append(tmp)
    
    frames = [np.random.randint(0, 256, (height, width), dtype=np.uint8)]
    for i in range(15):
        frame_pixels = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                if arr[y-1][x-1]:
                    frame_pixels[y, x] = np.random.randint(0, 256)
                else:
                    frame_pixels[y, x] = (frames[-1][y - arr[y][x], x - arr[y][x]])
        frames.append(frame_pixels)

    encrypted_frames = []
    password = password.encode().hex()
    for i, frame in enumerate(frames):
        key = PBKDF2(password[i], b'salt', dkLen=16, count=1000)
        cipher = AES.new(key, AES.MODE_ECB)
        data = frame.tobytes()

        encrypted = cipher.encrypt(data)
        encrypted_frames.append(encrypted.hex())
    
    return encrypted_frames

image = Image.open("flag.png")
image_gray = image.convert("L")
width, height = image.size

password = #REDACTED

encFrames = encrypt(image_gray, password)
print(f'height = {height}')
print(f'width = {width}')
print(f'enc = {encFrames}')