exec(open("output").read())

enc = [bytes.fromhex(e) for e in enc]

def xor_bytes(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

# for j in range(len(enc)):
#     for i in range(5):
#         cipher = xor_bytes(enc[j], enc[i])
#         known  = b"CBC{"
#         print(xor_bytes(cipher[:len(known)], known))
#     print(j) #7
#     print()

enc_flag = enc[7]
known = b"But that the dread of something after death," #2
cipher = xor_bytes(enc_flag, enc[2])
print(xor_bytes(cipher[:len(known)], known))