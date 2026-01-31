def xor_chained(data, keys):
    for k in keys:
        data = bytes(d ^ k.encode()[i % len(k)] for i, d in enumerate(data))
    return data

with open('flag.enc', 'rb') as f:
    data = f.read()
with open('keys.txt', 'r') as f:
    keys = [line.strip() for line in f]

result = xor_chained(data, keys)
try:
    print(result.decode())
except UnicodeDecodeError:
    print(result.hex())
