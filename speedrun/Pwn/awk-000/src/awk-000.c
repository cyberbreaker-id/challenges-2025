

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main() {
    init();

    puts("AWK: Anywhere Write KEK");
    printf("Biar gak pusing: %p\n", printf);

    int index = 0;
    long long arr[0x10];
    while(1) {

        printf("Index: ");
        scanf("%d", &index);
        printf("Value: ");
        scanf("%lld", &arr[index]);

        printf("Index %d value set to %lld\n", index, arr[index]);
    }
 

    return 0;
}

