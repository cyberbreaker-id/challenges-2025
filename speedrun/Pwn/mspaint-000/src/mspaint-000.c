

#include<stdio.h>
#include<stdlib.h>

struct canvas {
    size_t size_x;
    size_t size_y;
    char *data;
};

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void clear_canvas(struct canvas my_canvas) {
    for(size_t i = 0; i < my_canvas.size_y; i++) {
        for(size_t j = 0; j < my_canvas.size_x; j++) {
            my_canvas.data[i*my_canvas.size_y + j] = '.';
        }
    }

}

void print_canvas(struct canvas my_canvas) {
    puts("Current canvas:");
    for(size_t i = 0; i < my_canvas.size_y; i++) {
        for(size_t j = 0; j < my_canvas.size_x; j++) {
            putc(my_canvas.data[i*my_canvas.size_y + j], stdout);
        }
        putc('\n', stdout);
    }
    printf("> ");
}

void print_help() {
    puts("Usage: [OPERATION] [ARGS]");
    puts("Valid operations:");
    puts(" p [arg1] [arg2] [arg3], paints arg3 index canvas[arg1][arg2], arg3 must be a hexadecimal value");
    puts(" r [arg1] [arg2]       , resizes canvas to canvas of size arg1 x arg2 (DEFAULT: 20 x 20)");
    puts(" h                     , display this help");
    puts(" e                     , exit the program");
}

static void inline flush_stdin() {
    int res;
    while ((res = getchar()) != '\n' && res != EOF );
}

int main(int argc, char *argv[]) {

    init();
    struct canvas my_canvas = {
        .size_x = 20,
        .size_y = 20,
        .data = alloca(20*20)
    };

    char op, arg3;
    int res, arg1, arg2;
    clear_canvas(my_canvas);

    while(1) {
        print_canvas(my_canvas);
        res = scanf("%1s", &op);
        if(res != 1) { op = '\0'; }
        switch(op) {
            case 'p':
                res = scanf("%d %d %hhx", &arg1, &arg2, &arg3);
                if(res != 3) {
                    puts("Invalid operation. 'h' for help");
                    flush_stdin();
                    break;
                }
                if(my_canvas.data[arg1*my_canvas.size_y + arg2] == '.')
                    my_canvas.data[arg1*my_canvas.size_y + arg2] = arg3;
                break;
            case 'r':
                res = scanf("%d %d", &arg1, &arg2);
                if(res != 2) {
                    puts("Invalid operation. 'h' for help");
                    flush_stdin();
                    break;
                }

                void *new_data = alloca(arg1 * arg2);
                if(new_data == NULL) {
                    puts("Internal Server Error");
                    exit(1);
                }
                my_canvas.data = new_data;
                my_canvas.size_x = arg2;
                my_canvas.size_y = arg1;
                clear_canvas(my_canvas);
                puts("Canvas Resized and Reset!");
                break;
            case 'h':
                print_help();
                break;
            case 'e':
                puts("Bye");
                return 0;
            default:
                puts("Invalid operation. 'h' for help");
                flush_stdin();
                break;
        }
    }


    return 0;
}
