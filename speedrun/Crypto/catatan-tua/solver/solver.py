c = open("tjatatan.txt", "r").read()
keyMap = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
plnMap = list("JDFOIFR_GWBANPKTMSC__LEH__")


plaintext = []
for char in c:
    if char.upper() in keyMap:
        index = keyMap.index(char.upper())
        plain_char = plnMap[index]
        if char.islower():
            plain_char = plain_char.lower()
        plaintext.append(plain_char)
    else:
        plaintext.append(char)
print("".join(plaintext))