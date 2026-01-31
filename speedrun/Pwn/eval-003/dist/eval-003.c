#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/prctl.h>

#define MAX_SHELLCODE_LEN 0x1000

void *shellcode;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    shellcode = mmap(NULL, MAX_SHELLCODE_LEN, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);
    if(shellcode == NULL) {
        puts("Error, contact admin if on remote");
        exit(-1);
    }
}

int valid(char *shellcode) {
    return 1;
}

void setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (ctx == NULL) {
        puts("seccomp_init failed");
        exit(-1);
    }

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(writev), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pread64), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwrite64), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(preadv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwritev), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(preadv2), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pwritev2), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);

    if (seccomp_load(ctx) < 0) {
        puts("seccomp_load failed");
        exit(-1);
    }

    seccomp_release(ctx);
}

int main() {
    init();

    printf("Enter shellcode: ");
    read(0, shellcode, MAX_SHELLCODE_LEN);

    if(valid((char*)shellcode)) {
        setup_seccomp();

        (*(void(*)()) shellcode)();

    } else {
        puts("No.");
    }

    return 0;
}
