
// gcc -fno-stack-protector -no-pie -z relro -z now -o mixup mixup.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>

static void op0(const char *arg){ puts(arg); }
static void op1(const char *arg){ puts(arg); }
static void op2(const char *arg){ puts(arg); }
static void op3(const char *arg){ puts(arg); }

typedef void (*op_t)(const char *);   // <-- make ops take a string

struct S {
    char names[4][16];
    op_t ops[4];
};

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    struct S s; memset(&s, 0, sizeof(s));
    strcpy(s.names[0], "alpha");
    strcpy(s.names[1], "beta");
    strcpy(s.names[2], "gamma");
    strcpy(s.names[3], "delta");
    s.ops[0]=op0; s.ops[1]=op1; s.ops[2]=op2; s.ops[3]=op3;

    puts("== swap-mixup ==");
    puts("Commands: rename <idx> <len> then <len> bytes; do <idx>; list; quit");
    char cmd[16];
    int idx; unsigned int len;
    while(1){
        printf("> ");
        if(scanf("%15s", cmd)!=1) break;
        if(!strcmp(cmd,"rename")){
            if(scanf("%d %u", &idx, &len)!=2) break;
            if(idx<0 || idx>=4){ puts("bad"); continue; }
            char tmp[1024]={0};
            read(0, tmp, len);
            memcpy(s.names[idx], tmp, len);
            puts("ok");
        } else if(!strcmp(cmd,"do")){
            if(scanf("%d",&idx)!=1) break;
            if(idx<0 || idx>=4){ puts("bad"); continue; }
            s.ops[idx](s.names[idx]);
        } else if(!strcmp(cmd,"list")){
            for(int i=0;i<4;i++) printf("%d: %s\n", i, s.names[i]);
        } else if(!strcmp(cmd,"quit")){
            break;
        } else puts("?");
    }
    return 0;
}
