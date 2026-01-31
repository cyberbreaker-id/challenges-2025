// gcc awk-002.c -o awk-002 -no-pie -Wl,-z,relro,-z,lazy

#include<stdio.h>
#include<stdlib.h>
#include<sys/mman.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

// biar gak terlalu ribet 
void win() {
    system("/bin/sh");
}

int main(int argc, char *argv[]) {
    init();

    puts("Anywhere Write KEK");
    puts("No more easy stuff, this time the array is in heap and you cant escape >:)");

    long long *arr = malloc(0x10 * sizeof(unsigned long long));

    long long index = 0;
    while(1) {
        
        printf("Index: ");
        scanf("%lld", &index);
        printf("Value: ");
        scanf("%lld", &arr[index]);

        printf("Index %lld value set to %lld\n", index, arr[index]);
    }

    return 0;
}
