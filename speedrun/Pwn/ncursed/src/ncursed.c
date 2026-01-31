#include <ncurses.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void print_banner(WINDOW *w) {
    mvwprintw(w, 1, 2, "=== Greeter ===");
    mvwprintw(w, 2, 2, "1) Enter your name");
    mvwprintw(w, 3, 2, "2) Show greeting");
    mvwprintw(w, 4, 2, "3) Quit");
    box(w, 0, 0);
    wrefresh(w);
}

void secret(WINDOW *w) {
    FILE *fp = fopen("flag.txt", "r");
    char flag[256];

    werase(w);
    box(w, 0, 0);

    if (fp == NULL) {
        mvwprintw(w, 1, 2, "Error: could not open flag file.");
    } else {
        if (fgets(flag, sizeof(flag), fp) != NULL) {
            mvwprintw(w, 1, 2, "Congrats, here's the flag:");
            mvwprintw(w, 2, 2, "%s", flag);
        } else {
            mvwprintw(w, 1, 2, "Error: flag file empty.");
        }
        fclose(fp);
    }

    wrefresh(w);
}

int main() {
    if (!getenv("TERM")) {
        setenv("TERM", "xterm-256color", 1);
    }

    initscr();
    noecho();
    cbreak();

    WINDOW *menu = newwin(10, 50, 1, 1);
    keypad(menu, TRUE);

    char name[64];
    int is_admin = 0;
    int ch = 0;

    memset(name, 0, sizeof(name));
    strncpy(name, "guest", sizeof(name) - 1);

    while (1) {
        werase(menu);
        print_banner(menu);
        mvwprintw(menu, 6, 2, "Current user: %s", name);
        // if (is_admin == 0xff) {
        //     mvwprintw(menu, 7, 2, "[admin]");
        // } else {
        //     mvwprintw(menu, 7, 2, "[user]");
        // }
        wrefresh(menu);

        mvwprintw(menu, 8, 2, "Choice: ");
        wrefresh(menu);

        ch = wgetch(menu);
        if (ch == '1') {
            mvwprintw(menu, 8, 2, "Enter name: ");
	    wclrtoeol(menu);
            wrefresh(menu);

	    echo();
            wgetnstr(menu, name, 200);
	    noecho();
        } else if (ch == '2') {
            werase(menu);
            box(menu, 0, 0);

            if (is_admin == 0xff) {
                secret(menu);
            } else {
                mvwprintw(menu, 1, 2, "Hello, %s!", name);
                mvwprintw(menu, 3, 2, "You are not admin. Try again!");
                wrefresh(menu);
            }

            mvwprintw(menu, 8, 2, "Press any key to continue...");
            wgetch(menu);
        } else if (ch == '3') {
            break;
        }
    }

    delwin(menu);
    endwin();
    return 0;
}

