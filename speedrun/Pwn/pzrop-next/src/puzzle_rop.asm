; puzzle_rop.asm — NASM x86_64 Linux
; Build: see Makefile below
; Properties: NX stack, no PIE, no canary. Intended gadgets provided.

BITS 64
DEFAULT REL

GLOBAL _start



SECTION .text

_start:

    call vuln

    mov rax, 60         ; SYS_exit
    xor rdi, rdi
    syscall

vuln:
    push rbp
    mov rbp, rsp
    sub rsp, 0x80
    call maybe_banner
    xor rax, rax
    xor rdi, rdi
    lea rsi, [rel pay]
    mov rdx, 0x400
    syscall
    lea rdi, [rel pay]
    call [rdi]


    leave
    ret

pop_rdi_ret:
    pop rdi
    ret

pop_rsi_ret:
    pop rsi
    ret

pop_rax_ret:
    pop rax
    ret

; Useful transforms
xor_rsi_rsi_ret:
    xor rsi, rsi
    ret

xor_rdx_rdx_ret:
    xor rdx, rdx
    ret

xchg_rax_rdx_ret:
    xchg rax, rdx
    ret

g_a1b2c3:
    pop rcx
    pop rax
    ret

g_d4e5f6:
    xchg rax, rbx
    ret

g_102938:
    add rsp, 0x10
    ret

g_abcdef:
    mov rdi, rsi
    ret

g_112233:
    mov rax, rcx
    ret

g_445566:
    xor rbx, rbx
    ret

g_778899:
    push rdi
    pop rsi
    ret

g_aabbcc:
    mov rdx, rbx
    ret

g_ddeeff:
    xchg rsi, rdi
    ret

g_f00d42:
    nop
    ret

g_mem01:
    mov rax, [rdi]
    ret

g_mem02:
    mov [rsi], rax
    ret

g_mem03:
    mov rcx, [rdx]
    ret

g_mem04:
    mov [rbx], rcx
    ret

g_dead05:
    pop rsp
    pop rcx
    ret

g_dead0a:
    push rdi
    mov rax, [rdi + 0x10]
    jmp rax

; Syscall trampoline
syscall_ret:
    syscall
    ret

maybe_banner:
    push rbp
    mov rbp, rsp
    mov rax, 1          ; SYS_write
    mov rdi, 1          ; fd = stdout
    lea rsi, [rel msg]
    mov rdx, msg_end - msg
    syscall
    pop rbp
    ret


SECTION .rodata
msg: db "Welcome to puzzle-rop! Overflow me.", 10
msg_end:
binsh: db "/bin/sh",0

SECTION .bss
pay:  db 0

; Mark a GNU stack note so the linker marks the stack as non-exec by default
SECTION .note.GNU-stack noalloc noexec nowrite progbits
