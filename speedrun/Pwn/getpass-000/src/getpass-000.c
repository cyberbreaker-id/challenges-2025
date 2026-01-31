

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/random.h>

char password[0x10];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    getrandom(password, 0x10, 0);
}

int main() {
    init();

    char input[0x100];
    puts("Welcome to flag inc. What's the password?");

    printf("Password: ");
    fgets(input, 0x100, stdin);
    if(strcmp(input, password) == 0) {
        system("cat flag.txt; sleep 5");
        return 0;
    } else {
        puts("Nope! Wrong password");
    }

    return 0;
}

