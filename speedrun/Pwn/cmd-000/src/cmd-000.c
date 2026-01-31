

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

#define MAX_BUF 0x100

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void read_str(char *buf) {
    memset(buf , 0, MAX_BUF);
    char *line = NULL;
    size_t len = 0;
    if(getline(&line, &len, stdin) < 0) {
        exit(-1);
    }
    strncpy(buf, line, MAX_BUF);
    for(size_t i = 0; i < MAX_BUF; i++) {
        if (!isalnum(buf[i]) && !isspace(buf[i]) && buf[i] != '/' && buf[i] != '.' && buf[i] != '\0') {
            puts("No");
            exit(-1);
        }
    }
    buf[len] = '\0';
}

void menu() {
    puts("1. pwd");
    puts("2. md5sum <file>");
    puts("3. sha256sum <file>");
    puts("4. echo <string>");
    puts("5. sleep <seconds>");
    puts("6. whoami");
    puts("7. id");
    puts("8. realpath <file>");
    printf("Choice (number): ");
}

int main() {
    init();

    char formats[8][20] = {
        "pwd",
        "md5sum %s",
        "sha256sum %s",
        "echo %s",
        "sleep %d",
        "whoami",
        "id",
        "realpath %s"
    };

    char buf[MAX_BUF] = {0};
    char tmp[MAX_BUF] = {0};
    int choice = 0;
    while(1) {
        menu();
        read_str(buf);
        choice = atoi(buf);
        switch(choice) {
            case 1:
                sprintf(buf, formats[choice-1]);
                system(buf);
                break;
            case 2:
                printf("Filename: ");
                read_str(tmp);
                sprintf(buf, formats[choice-1], tmp);
                system(buf);
                break;
            case 3:
                printf("Filename: ");
                read_str(tmp);
                sprintf(buf, formats[choice-1], tmp);
                system(buf);
                break;
            case 4:
                printf("String: ");
                read_str(tmp);
                sprintf(buf, formats[choice-1], tmp);
                system(buf);
                break;
            case 5:
                printf("Seconds: ");
                read_str(tmp);
                int sleep = atoi(tmp);
                sprintf(buf, formats[choice-1], sleep);
                system(buf);
                break;
            case 6:
                sprintf(buf, formats[choice-1]);
                system(buf);
                break;
            case 7:
                sprintf(buf, formats[choice-1]);
                system(buf);
                break;
            case 8:
                printf("Filename: ");
                read_str(tmp);
                sprintf(buf, formats[choice-1], tmp);
                system(buf);
                break;
        }
    }

    return 0;
}

