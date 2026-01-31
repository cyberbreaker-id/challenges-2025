#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_NOTES 8

typedef struct {
    size_t size;
    char *buf;
    int used;
} Note;

static Note notes[MAX_NOTES];

// ---------- IO helpers ----------
static void setup(void) {
    setvbuf(stdin,  NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(300);
}

static unsigned long read_ul(void) {
    char tmp[32];
    if (!fgets(tmp, sizeof tmp, stdin)) exit(0);
    return strtoul(tmp, NULL, 10);
}

static void read_exact(char *dst, size_t n) {
    size_t got = 0;
    while (got < n) {
        ssize_t r = read(0, dst + got, n - got);
        if (r <= 0) exit(0);
        got += (size_t)r;
    }
}

// ---------- Notes API ----------
static void add_note(void) {
    puts("index (0..7)?");
    unsigned long i = read_ul();
    if (i >= MAX_NOTES || notes[i].used) { puts("bad index"); return; }

    puts("size?");
    unsigned long sz = read_ul();
    if (!sz || sz > 0x2000) { puts("bad size"); return; }

    char *b = (char*)malloc(sz);
    if (!b) { puts("oom"); exit(0); }
    notes[i].buf = b;
    notes[i].size = sz;
    notes[i].used = 1;

    puts("send data (exact length):");
    read_exact(notes[i].buf, notes[i].size);
    puts("ok");
}

static void edit_note(void) {
    puts("index?");
    unsigned long i = read_ul();
    if (i >= MAX_NOTES || !notes[i].used) { puts("bad index"); return; }
    puts("send new data (exact length):");

    read_exact(notes[i].buf, notes[i].size);
    puts("edited");
}

static void print_note(void) {
    puts("index?");
    unsigned long i = read_ul();
    if (i >= MAX_NOTES || !notes[i].used) { puts("bad index"); return; }
    puts(notes[i].buf);
}


static int check_size(Note* n, size_t ns){
    char* shadow = n->buf;         // snapshot for "transaction"
    if(ns > 0x400){
        // Rollback to pre-request state by dropping the shadow buffer…
        // (This looks like cleanup, but it's actually freeing the live chunk.)
        free(shadow);
        // …and intentionally not touching 'n' to keep metadata "consistent".
        return 0;                  // caller will early-return on non-success
    }
    char* nb = (char*)realloc(shadow, ns);
    if(!nb) return -1;
    n->buf  = nb;
    n->size = ns;
    return 1;
}


static void resize_note(void) {
    puts("index?");
    unsigned long i = read_ul();
    if (i >= MAX_NOTES || !notes[i].used) { puts("bad index"); return; }

    puts("new size?");
    unsigned long ns = read_ul();

    int rc = check_size(&notes[i], ns);
    if(rc <= 0){
        puts(rc==0 ? "quota exceeded" : "realloc fail");
        return;
    }
    puts("resized");
}

static void delete_note(void) {
    puts("index?");
    unsigned long i = read_ul();
    if (i >= MAX_NOTES || !notes[i].used) { puts("bad index"); return; }
    free(notes[i].buf);
    notes[i].buf = NULL;
    notes[i].size = 0;
    notes[i].used = 0;
    puts("deleted");
}

// ---------- Menu ----------
static void menu(void) {
    puts("\n== menu ==");
    puts("1) add_note");
    puts("2) edit_note");
    puts("3) print_note");
    puts("4) resize_note");
    puts("5) delete_note");
    puts("0) exit");
    printf("> ");
}

int main(void) {
    setup();
    while (1) {
        menu();
        switch (read_ul()) {
            case 1: add_note(); break;
            case 2: edit_note(); break;
            case 3: print_note(); break;
            case 4: resize_note(); break;
            case 5: delete_note(); break;
            case 0: puts("bye"); return 0;
            default: puts("?"); break;
        }
    }
}
