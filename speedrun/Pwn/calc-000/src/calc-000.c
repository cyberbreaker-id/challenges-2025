

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>


void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void calc(char *buf) {
    long long num0, num1, num2, num3, num4, sum;
    sscanf(buf, " %lld %lld %lld %lld %lld", &num0, &num1, &num2, &num3, &num4);
    sum = num0 + num1 + num2 + num3 + num4;
    printf("Sum: %lld\n", sum);
    return;
}


int main() {
    init();

    char buf[0x100];
    double num1, num2, result;
    char op;

    while(1) {
        puts("Give me 5 numbers and I will sum them all");
        fgets(buf, 0x1000, stdin);
        if(strncmp(buf, "exit", 4) == 0) break;
        calc(buf);
    }
    return 0;
}

