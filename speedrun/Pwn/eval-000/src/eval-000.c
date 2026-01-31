

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/mman.h>
#include<unistd.h>

void *shellcode;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    shellcode = mmap(NULL, 0x1000, 7, MAP_PRIVATE | MAP_ANON, -1, 0);
    if(shellcode == NULL) {
        puts("Error, contact admin if on remote");
        exit(-1);
    }
}

int valid(char *shellcode) {

    for(int i = 0; i < 0x1000; i++) {
        if(shellcode[i] == 0xf || shellcode[i] == 0x5 || shellcode[i] == 0x80 || shellcode[i] == 0xcd) {
            return 0;
        }
    }
    return 1;
}

int main() {
    init();

    printf("Enter shellcode: ");
    read(0, shellcode, 0x1000);

    if(valid((char*)shellcode)) {
        puts("Ok I hope you got a shell :)");

        (*(void(*)()) shellcode)();

    } else {
        puts("No.");
    }
 

    return 0;
}

