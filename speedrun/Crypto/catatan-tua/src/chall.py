import random

plaintext = """
     Tjatatan Misi Rahasia

Jogjakarta, 12 Agoestoes 1908:
Malam ini kami bertolak. Hawa terasa genting, sarat dengan asa dan djoega kebimbangan. Semoea kawan telah sedia. Wadjah mereka tampak kakoe di bawah tjahaja remboelan. Semoga jang maha koeasa merahmati kami. Demi soerat siasat itoe. Demi hari esok jang lebih baik.

Jogjakarta, 13 Agoestoes 1908:
Tertjapai. Soerat siasat itoe kini dalam genggaman kami. Saja simpan dengan saksama di dalam peti timah. Kini, oedjian terberat: keloear dari tempat tjelaka ini dengan selamat.

Jogjakarta, 13 Agoestoes 1908:
Kompeni mengepoeng kami. Semoea kawan telah goegoer. Hanja saja jang berhasil kaboer.
Soerat siasat itoe wadjib diselamatkan. Djika kelak kaoe menemoekannja, sandi rahasianja adalah:

CBC{doEs_oPhoeiseN_tjan_BeaAts_AI???_JDFOIRGWBANPKTMSCLEH}

Maafkan saja, Ratri. Koetitipkan poetra kita. Maaf Bapak tak akan kembali.
"""

keyMap = list("LKSBWCIXEAOVQMDNZGRPTFJUHY")
plainMap = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

enc = []
for char in plaintext:
    if char.upper() in plainMap:
        index = plainMap.index(char.upper())
        enc_char = keyMap[index]
        if char.islower():
            enc_char = enc_char.lower()
        enc.append(enc_char)
    else:
        enc.append(char)

print("".join(enc))
