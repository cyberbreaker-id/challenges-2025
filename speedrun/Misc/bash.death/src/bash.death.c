

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void command(char *buf) {

    for(size_t i = 0; i < strlen(buf); i++) {
        if(buf[i] == ';') {
            puts("No.");
            exit(1);
        }
    }

    char *command = malloc(0x200);
    sprintf(command, "printf %s", buf);
    system(command);
    return;
}

int main() {
    init();

    puts("printf as a service");
    printf("Input: ");

    char buf[0x100];
    fgets(buf, 0x100, stdin);

    printf("Output: ");
    command(buf);

    return 0;
}

