#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_COMMAND_LEN 256
#define MAX_DATA_LEN 128

static void init(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
}

static void shell() {
    execve("/bin/sh", NULL, NULL);
}

static int get_user_input(char *buffer, size_t size) {
    if (fgets(buffer, size, stdin) == NULL) {
        return 0;
    }
    
    buffer[strcspn(buffer, "\n")] = '\0';
    return 1;
}

static void show_prompt(void) {
    printf("vault> ");
}

static void cmd_write(char *data, char *path) {
    if (path && strstr(path, "flag.txt") != NULL) {
        printf("Restricted\n");
        return;
    }
    
    char buffer[MAX_DATA_LEN];
    strcpy(buffer, data);

    printf("Data written to %s: %s\n", path, buffer);
}

static void cmd_read(char *path) {
    if (path && strstr(path, "flag.txt") != NULL) {
        printf("Restricted\n");
        return;
    }

    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        printf("Failed to open file: %s\n", path);
        return;
    }

    char buffer[0x1000];
    size_t n = fread(buffer, 1, sizeof(buffer) - 1, fp);
    buffer[n] = '\0';
    fclose(fp);

    printf("Content of %s:\n%s\n", path, buffer);
}
 
static void cmd_help(void) {
    printf("Available commands:\n");
    printf("  read <path>                   - Read your vault content\n");
    printf("  write <data> <path>           - Write content to your vault\n");
    printf("  help                          - Show this help message\n");
    printf("  exit                          - Exit the program\n");
}

static int parse_command(char *input) {
    char *command = strtok(input, " ");
    if (command == NULL) {
        return -1;
    }
    
    if (strcmp(command, "read") == 0) {
        char *path = strtok(NULL, " ");
        cmd_read(path);
        return 1;
    } else if (strcmp(command, "write") == 0) {
        char *data = strtok(NULL, " ");
        char *path = strtok(NULL, " ");
        cmd_write(data, path);
        return 1;
    } else if (strcmp(command, "help") == 0) {
        cmd_help();
    } else if (strcmp(command, "exit") == 0) {
        printf("Goodbye!\n");
        exit(EXIT_SUCCESS);
        
    } else {
        printf("Unknown command: %s\n", command);
        printf("Type 'help' for available commands.\n");
    }

    return 0;
}

int main(void) {
    char input[MAX_COMMAND_LEN];
    
    init();
    
    printf("=== Vault System ===\n");
    printf("Type 'help' for available commands.\n");
    
    while (1) {
        show_prompt();
        
        if(!get_user_input(input, sizeof(input))) {
            break;
        }

        int ret = parse_command(input);
        if (ret) break;
    }
    
    return EXIT_SUCCESS;
}