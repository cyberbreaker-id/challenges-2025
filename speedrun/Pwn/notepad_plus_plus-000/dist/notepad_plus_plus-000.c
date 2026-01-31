

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_RESET   "\x1b[0m"

struct note {
    int (*func)(const char *);
    char data[100];
};

struct note *notes[0x10];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void menu() {
    puts("1. Create Note");
    puts("2. Print Note");
    puts("3. Delete Note");
    puts("4. Exit");
    printf("> ");
}

void print_note_types() {
    puts("1. Regular Note");
    puts("2. Invisible Note");
    printf("Type: ");
}

int get_int() {
    char buf[0x10];
    fgets(buf, 0x10, stdin);
    return atoi(buf);
}

void create_note() {
    int index = 0;
    printf("Index: ");
    index = get_int();

    int note_type = -1;
    print_note_types();
    note_type = get_int();
    
    notes[index] = malloc(sizeof(struct note));
    
    char *buf = notes[index]->data;
    printf("Note data: ");
    fgets(buf, 0x100, stdin);
    

    switch(note_type) {
        case 1:
            sprintf(buf, "%s", buf);
            notes[index]->func = puts;
            break;
        case 2:
            buf[0] = '\0';
            notes[index]->func = puts;
            break;
        default:
            notes[index]->func = printf;
            break;
    }

}

void print_note() {
    int index = 0;
    printf("Index: ");
    index = get_int();
    
    notes[index]->func(notes[index]->data);
    puts("Done!");
}

void delete_note() {
    int index = 0;
    printf("Index: ");
    index = get_int();
    
    free(notes[index]);
    notes[index] = NULL;
    puts("Done!");

}

int main() {
    init();
    
    int choice = 0;
    while(1) {
        menu();
        choice = get_int();
        switch(choice) {
            case 1:
                create_note();
                break;
            case 2:
                print_note();
                break;
            case 3:
                delete_note();
                break;
            default:
                break;
        }
    }
    return 0;
}

