
// gcc -no-pie -z relro -z now -o mazerunner mazerunner.c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void safe(){
    puts("Nothing happens...");
}

void __attribute__((noinline)) win(void){
    puts("You found the hidden path!");
    system("/bin/sh");
}

typedef struct {
    char grid[8][8];
    void (*act)(void);
} Game;

void draw(Game *g){
    for(int y=0;y<8;y++){
        for(int x=0;x<8;x++){
            char c = g->grid[y][x];
            if(c==0) c='.';
            putchar(c);
        }
        putchar('\n');
    }
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    Game g; memset(&g, 0, sizeof(g));
    g.act = safe;

    puts("== maze-runner-oob ==");
    puts("Commands:");
    puts("  P x y ch  -> place char at (x,y)");
    puts("  A         -> act()");
    puts("  D         -> draw");
    puts("  Q         -> quit");
    puts("");
    puts("Hint: it's easy to make a mistake near the right border...");

    char cmd[4];
    while(1){
        printf("> ");
        if(scanf("%3s", cmd)!=1) return 0;
        if(cmd[0]=='Q') break;
        if(cmd[0]=='D'){
            draw(&g);
        } else if(cmd[0]=='A'){
            puts("Acting...");
            g.act();
        } else if(cmd[0]=='P'){
            int x,y; unsigned char ch;
            if(scanf("%d %d %hhu", &x, &y, &ch)!=3) break;
            if((x >= 0 && x <= 8) && (y >= 0 && y < 8)){
                g.grid[y][x] = (char)ch;
                puts("ok");
            }else{
                puts("nope");
            }
        } else {
            puts("??");
        }
    }
    return 0;
}
