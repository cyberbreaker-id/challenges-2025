

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void echo() {

    char input[0x100];

    printf("Input: ");
    fgets(input, 0x100, stdin);
    input[strcspn(input, "\n")] = '\0';
    
    for(int i = 0; i < strlen(input); i++) {
        if(input[i] == ' ') continue; // space is allowed
        input[i] = (input[i] % 26) + 0x61; // whitelist is better than blacklist
                                           // this guarantees ascii_lowercase :)
    }

    char *echo_command = malloc(0x200);
    sprintf(echo_command, "echo %s", input);
    system(echo_command);
    return;
}

int main() {
    init();

    puts("Echo as a service");

    echo();

    return 0;
}

