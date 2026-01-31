

#include<stdio.h>
#include<stdlib.h>

#define MAX_BUF 0x100

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void win() {
    system("cat flag.txt");
    system("/bin/sh");
}

int main() {
    init();

    long long address, value;
    printf("Address: ");
    scanf("%lld", &address);
    printf("Value: ");
    scanf("%lld", &value);

    *(long long *)address = value;

    puts("bye!");
    return 0;
}

