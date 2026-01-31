; puzzle_rop.asm — NASM x86_64 Linux
; Build: see Makefile below
; Properties: NX stack, no PIE, no canary. Intended gadgets provided.

BITS 64
DEFAULT REL

GLOBAL _start

SECTION .text

_start:

    lea rdi, [rel flagname]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 2          ; SYS_open ; flag opened for you
    syscall

    mov rax, 157        ; SYS_prctl
    mov rdi, 22         ; PR_SET_SECCOMP
    mov rsi, 1          ; SECCOMP_MODE_STRICT
    xor rdx, rdx
    syscall             ; read/write only

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
    mov rsi, rsp
    mov rdx, 0x400
    syscall

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

xor_rsi_rsi_ret:
    xor rsi, rsi
    ret

xor_rdx_rdx_ret:
    xor rdx, rdx
    ret

xchg_rax_rdx_ret:
    xchg rax, rdx
    ret

add_rax_1_ret:
    add rax, 1
    ret

g_1a2b3c:
    pop rbx
    ret

g_4d5e6f:
    inc rsi
    ret

g_7c8d9e:
    dec rdx
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

g_123321:
    sub rsp, 8
    ret

g_654321:
    add rax, 1
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

g_mem05:
    mov rdx, [rsp+8]
    ret

g_dead01:
    jmp rax

g_dead02:
    jmp rcx

g_dead03:
    jmp [rdi]

g_dead04:
    call rbx

g_dead05:
    call [rdx]

g_dead06:
    jmp [rsp]

g_dead07:
    mov rax, [rsi]
    jmp rax

g_dead08:
    push rbx
    ret

g_dead09:
    xchg rax, rcx
    jmp rcx

g_dead0a:
    mov rax, [rdx]
    call rax

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

flagname: db "flag.txt", 0

SECTION .bss
x: db 0
; Mark a GNU stack note so the linker marks the stack as non-exec by default
SECTION .note.GNU-stack noalloc noexec nowrite progbits
