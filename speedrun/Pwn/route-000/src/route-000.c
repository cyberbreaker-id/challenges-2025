// gcc route-000.c -o route-000 -no-pie -fno-stack-protector

#include<stdio.h>
#include<stdlib.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void win(char *cmd, long long arg1, long long arg2) {
    if(arg1 == 0x847df05444ca91ae && arg2 == 0xf865894831cca075) {
        system(cmd);
    }
}

int main() {
    init();
    char buf[0x10];
    printf("Easy ret2win: ");
    read(0, buf, 0x28);
    return 0;
}