import random

def create_polybius_square():
    chrMap  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{_ ,.!'#*58}"
    polybius_square = [list(chrMap[i:i+8]) for i in range(0, 64, 8)]
    
    keyMap = list(range(8))
    random.shuffle(keyMap)

    shuffled_polybius = []
    for i in range(8):
        shuffled_row = []
        for j in range(8):
            shuffled_row.append(polybius_square[keyMap[i]][j])
        shuffled_polybius.append(shuffled_row)

    return shuffled_polybius

def find_position(c, polybius_square):
    for i in range(8):
        for j in range(8):
            if polybius_square[i][j] == c:
                return (i, j)

def encrypt(text, polybius_square):
    cipher = ""
    for char in text:
        r, c = find_position(char, polybius_square)
        cipher += str(r) + str(c)
    return cipher

polybius_square = create_polybius_square()
plaintext = "I cant encrypt my flag using The Classic _5x5_ grid. An _8x8_ polybius square Became the perfect Choice for my flag! Anyway, here's the flag you're looking for CBC{CheckmAtE_on_the_CIphEr_BOArd}"
cipher = encrypt(plaintext, polybius_square)

print(f"cipher = '{cipher}'")
print(f"hint = '{plaintext[:118]}'")
