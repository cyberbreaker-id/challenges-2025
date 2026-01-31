from itertools import permutations

cipher = "8nmndewamovhkkjpi8brgc9v3fjixi4pjk_un}n5yvry6t1t4ouyfd6hm88vjlfyhs{s1rj3kf6m$0_hih"
knownPlaintext = "just keep walking and you can see that the flag is"

for i in range(1, len(knownPlaintext)):
    if knownPlaintext[i] == knownPlaintext[i-1]:
        knownPlaintext = knownPlaintext[:i] + '$' + knownPlaintext[i+1:]

plainMap = "abcdefghijklmnopqrstuvwxyz0123456789_{}$ "


plain_num = []
for i, c in enumerate(knownPlaintext):
    plain_num.append(plainMap.index(c))

secret = ['-'] * 40
long = 0
short = 0
for i, c in enumerate(plain_num):
    step = (c - long) % 41
    long = c
    short = (short + step) % 40
    secret[short] = cipher[i]

print("".join(secret))
# 5da-o-hw-8bcefgijk-mnp-r-tuvxy-1-3469_-}
secret = list("5da-o-hw-8bcefgijklmnpqrstuvxy-123469_{}")
choice = list("0z7$")

for perm in permutations(choice, 4):
    newSecret = []
    for i in range(len(secret)):
        if secret[i] == "-":
            newSecret.append(perm[0])
            perm = perm[1:]
        else:
            newSecret.append(secret[i])

    secretMap = {}
    for i, c in enumerate(newSecret):
        secretMap[c] = i

    plain = ''
    long = 0
    short = 0
    for i, c in enumerate(cipher):
        try:
            step = (secretMap[c] - short) % 40
            short = secretMap[c]
            if step == 0:
                step -= 1
            long = (long + step) % 41
            plain += plainMap[long]
        except:
            plain += '_'

    print(plain)
        