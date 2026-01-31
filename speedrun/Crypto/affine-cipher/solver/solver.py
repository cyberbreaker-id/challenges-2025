exec(open("output").read())

chrMap  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{_}"

def affine_decrypt(cipher, key):
    plain = ""
    mod_inv = pow(key[0], -1, len(chrMap))
    for c in cipher:
        plain += chrMap[(mod_inv * ((chrMap.index(c) - key[1]) % len(chrMap))) % len(chrMap)]
    return plain

for i in range(65):
    for j in range(65):
        try:
            possible_key = [i, j]
            decrypted = affine_decrypt(cipher, possible_key)
            if decrypted.startswith("CBC{"):
                print(decrypted)
                break
        except:
            continue