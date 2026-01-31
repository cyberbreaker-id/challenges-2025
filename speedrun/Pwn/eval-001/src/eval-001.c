

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/mman.h>
#include<unistd.h>

#define MAX_SHELLCODE_LEN 10

void *shellcode;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    shellcode = mmap(NULL, MAX_SHELLCODE_LEN, 7, MAP_PRIVATE | MAP_ANON, -1, 0);
    if(shellcode == NULL) {
        puts("Error, contact admin if on remote");
        exit(-1);
    }
}

int valid(char *shellcode) {

    for(int i = 0; i < MAX_SHELLCODE_LEN; i++) {
        if(shellcode[i] == 0x00) {
            return 0;
        }
    }
    return 1;
}

int main() {
    init();

    printf("Enter shellcode: ");
    read(0, shellcode, MAX_SHELLCODE_LEN);

    if(valid((char*)shellcode)) {
        puts("Ok I hope you got a shell :)");

        (*(void(*)()) shellcode)();

    } else {
        puts("No.");
    }
 

    return 0;
}

