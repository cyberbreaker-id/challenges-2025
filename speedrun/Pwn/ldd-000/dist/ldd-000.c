// gcc ldd-000.c -o ldd-000 -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <sys/auxv.h>
#include <unistd.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main() {
    printf("ld leak = %p\n", (void *)getauxval(AT_BASE));
    puts("Now ROP!");

    char buf[0x10];
    read(0, buf, 0x1000);
    return 0;
}