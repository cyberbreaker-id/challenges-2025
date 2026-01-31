

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void echo(char* blacklist, int blacklist_len) {

    char input[100];

    printf("Input: ");
    fgets(input, 0x100, stdin);
    
    for(int i = 0; i < blacklist_len; i++) {
        for(int j = 0; j < strlen(input); j++) {
            if(input[j] == blacklist[i]) {
                puts("No.");
                exit(-1);
            }
        }
    }

    char *echo_command = malloc(0x200);
    sprintf(echo_command, "echo %s", input);
    system(echo_command);
    return;
}

int main() {
    init();

    puts("Echo as a service");
    char blacklist[] = "\"\'`|;{}!@#$%^&*()<>/\\:[]";

    echo(blacklist, sizeof(blacklist));

    return 0;
}

