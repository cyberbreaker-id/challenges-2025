import itertools

exec(open("output.txt").read())
knownPlain = hint

def decrypt(cipher, polybiusMap):
    plaintext = ""
    for i in range(0, len(cipher), 2):
        r = int(cipher[i])
        c = int(cipher[i+1])
        if polybiusMap[r][c] != -1:
            plaintext += polybiusMap[r][c]
        else:
            plaintext += "?"
    return plaintext

knownMap = [[-1 for _ in range(8)] for _ in range(8)]
for i in range(0, len(knownPlain)):
    r = int(cipher[2*i])
    c = int(cipher[2*i+1])
    knownMap[r][c] = knownPlain[i]

print(knownMap)
print(decrypt(cipher, knownMap))