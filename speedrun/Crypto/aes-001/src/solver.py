from Crypto.Cipher import AES
from itertools import product
from tqdm import tqdm

exec(open("output").read())
cipher = bytes.fromhex(cipher)
key = bytes.fromhex(key)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


cipher = list(chunks(cipher, 16))

known = b"Can you find it?"
for guess in tqdm(product(range(256), repeat=3)):
    test_key = key + bytes(guess)
    enc = AES.new(test_key, AES.MODE_CBC, iv=cipher[-2])
    try:
        decrypted = enc.decrypt(cipher[-1])
        if decrypted == known:
            for i in range(1, len(cipher)):
                enc = AES.new(test_key, AES.MODE_CBC, iv=cipher[i-1])
                decrypted = enc.decrypt(cipher[i])
                print(decrypted.decode(), end="")
            break            
    except Exception:
        continue