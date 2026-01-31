// gcc awk-001.c -o awk-001 -Wl,-z,relro,-z,lazy

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/mman.h>

long long arr[0x10];

void *init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    void *rwx_area = mmap(NULL, 0x1000, 7, 0x22, -1, 0);
    if(rwx_area == MAP_FAILED) {
        puts("Error, contact admin if remote");
        exit(-1);
    }
    return rwx_area;
}

int main() {
    void *rwx_area = init();

    puts("AWK: Anywhere Write KEK");
    printf("rwx area: %p\n", rwx_area);

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

