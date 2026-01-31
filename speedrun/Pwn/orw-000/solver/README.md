# TLDR

ORW - (O)nly (R)read (W)rite, with `read` is open file.

## Solve

Open multiple connection to read:

1. `/proc/self/stat` to get PID.
2. `/proc/{pid}/maps` to get PIE base address.
3. ROP to `shell` function to get remote code execution.
