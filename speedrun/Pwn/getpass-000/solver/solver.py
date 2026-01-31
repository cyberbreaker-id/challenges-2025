

from pwn import *


while(1):
    p = process("./getpass-000")

    p.sendlineafter(":", "\0")
    a = p.recvuntil("Nope", timeout=1)
    if(a == b''):
        p.interactive()
        p.close()
        break
    else:
        p.close()
