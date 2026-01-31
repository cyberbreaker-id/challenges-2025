import random

plainMap = "abcdefghijklmnopqrstuvwxyz0123456789_{}$ "
maps = "abcdefghijklmnopqrstuvwxyz0123456789_{}$"
key = random.sample(maps, 10)

for c in maps:
    if c not in key:
        key += c
        
flag = "just keep walking and you can see that the flag is c0ngr4ts_y0u_m4d3_1t_to_th3_end"
for i in range(1, len(flag)):
    if flag[i] == flag[i-1]:
        flag = flag[:i] + '$' + flag[i+1:]

keyMap = key * len(flag)
plainMap = plainMap * len(flag)
enc = ""
flag_pos = 0
for i in range(len(plainMap)):
    if plainMap[i] == flag[flag_pos]:
        enc += keyMap[i]
        flag_pos += 1
        if flag_pos >= len(flag):
            break

print("enc = ", enc)
# enc = "8nmndewamovhkkjpi8brgc9v3fjixi4pjk_un}n5yvry6t1t4ouyfd6hm88vjlfyhs{s1rj3kf6m$0_hih"