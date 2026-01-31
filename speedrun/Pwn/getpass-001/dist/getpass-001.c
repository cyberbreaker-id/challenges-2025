

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/random.h>
#include <stdint.h>

uint8_t password[0x10];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    getrandom(password, 0x10, 0);
    for(size_t i = 0; i < 0x10; i++) {
        password[i] = (password[i] % 26) + 0x41; // no more null byte issue!
    }
}

void read_str(char *buf) {
    memset(buf, 0, 0x100);
    char *line = NULL;
    size_t len = 0;
    if(getline(&line, &len, stdin) < 0) {
        exit(-1);
    }
    snprintf(buf, 0x100, line);
    free(line);
}

int main() {
    init();

    char input[0x100];
    puts("Welcome to flag inc. What's the password?");

    while(1) {
        printf("Password: ");
        read_str(input);
        if(strcmp(input, password) == 0) {
            system("cat flag.txt; sleep 5");
            return 0;
        } else {
            puts("Nope! Wrong password");
            //printf("Debug: %s\n", input);
        }
    }

    return 0;
}

