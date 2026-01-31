#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define SLEEP_MS 200
static char FLAG[128] = "CBC{SPEED_SPEED_SPEED_LINZ_IS_HERE}\n";

static void write_file(const char *p,const char *s){int fd=open(p,O_WRONLY|O_CREAT|O_TRUNC,0600);if(fd>=0){write(fd,s,strlen(s));close(fd);}}
static void init_fs(void){
    mkdir("db",0700); mkdir("db/admin",0700); mkdir("db/player",0700);
    write_file("db/admin/role","admin\n");
    struct stat st; if(lstat("db/player/role",&st)==-1||!S_ISREG(st.st_mode)){unlink("db/player/role");write_file("db/player/role","user\n");}
    FILE *f=fopen("flag.txt","rb"); if(f){size_t n=fread(FLAG,1,sizeof(FLAG)-1,f);FLAG[n]='\0';fclose(f);}
}
static void cmd_fix(void){unlink("db/player/role");write_file("db/player/role","user\n");}
static int cmd_link(void){unlink("db/player/role");return symlink("../admin/role","db/player/role");}
static void cmd_login(void){
    struct stat st; if(lstat("db/player/role",&st)==-1){puts("[err]");return;}
    if(!S_ISREG(st.st_mode)){puts("[-]");return;}
    usleep(SLEEP_MS*1000);
    int fd=open("db/player/role",O_RDONLY); if(fd==-1){puts("[err]");return;}
    char buf[16]={0}; read(fd,buf,sizeof(buf)-1); close(fd);
    if(!strncmp(buf,"admin",5)){printf("flag: %s",FLAG);} else {puts("user");}
}

int main(void){
    setvbuf(stdout,NULL,_IONBF,0);
    init_fs();
    char line[64];
    printf("> ");
    while(fgets(line,sizeof(line),stdin)){
        line[strcspn(line,"\r\n")]=0;
        if(!strcmp(line,"FIX")){cmd_fix();puts("[ok]");}
        else if(!strcmp(line,"LINK")){if(cmd_link()==-1)puts("[err]");else puts("[ok]");}
        else if(!strcmp(line,"LOGIN")){cmd_login();}
        else if(!strcmp(line,"QUIT")){puts("bye");break;}
        else puts("?");
        printf("> ");
    }
    return 0;
}
