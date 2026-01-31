

#include<stdio.h>
#include<stdlib.h>
#include<string.h>


char flag[0x100];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    FILE *fp = fopen("flag.txt", "r");
    if(fp == NULL) {
        puts("Error, contact admin");
        exit(-1);
    }
    fread(flag, 1, 0x100, fp); // Free flag?
    memset(flag, 0, 0x100); // lol no
}


int main() {
    init();

    char line[0x100];
    while(1) {
        if (fgets(line, sizeof(line), stdin) != NULL) {
            printf("\033[A\33[2K\r");
            printf(line);
        }
    }
    return 0;
}

