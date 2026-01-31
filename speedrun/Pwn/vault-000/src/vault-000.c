#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 512
#define MAX_USERNAME_LEN 15
#define MAX_PASSWORD_LEN 15
#define MAX_VAULT_LEN 256
#define MAX_COMMAND_LEN 512

typedef struct {
    unsigned char id;
    char username[MAX_USERNAME_LEN + 1];
    char password[MAX_PASSWORD_LEN + 1];
} User;

typedef struct {
    unsigned char id;
    char content[MAX_VAULT_LEN + 1];
} Vault;

static User users[MAX_USERS];
static Vault secret_vault[MAX_USERS];
static int user_count = 0;
static int is_logged_in = 0;
static int current_user_id = -1;

static void generate_random_string(char *str, int length) {
    FILE *fp = fopen("/dev/urandom", "r");
    if (fp == NULL) {
        perror("Failed to open /dev/urandom");
        exit(EXIT_FAILURE);
    }
    fread(str, 1, length, fp);
    fclose(fp);
}

static int register_user(const char *username, const char *password) {    
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, username) == 0) {
            return -1;
        }
    }
    
    users[user_count].id = user_count + 1;
    strncpy(users[user_count].username, username, MAX_USERNAME_LEN);
    users[user_count].username[MAX_USERNAME_LEN] = '\0';
    
    strncpy(users[user_count].password, password, MAX_PASSWORD_LEN);
    users[user_count].password[MAX_PASSWORD_LEN] = '\0';
    
    secret_vault[user_count].id = users[user_count].id;
    secret_vault[user_count].content[0] = '\0';

    printf("User %s registered successfully with id %d\n", username, users[user_count].id);
    
    user_count++;
    return 1;
}

static int authenticate_user(const char *username, const char *password) {
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, username) == 0 && 
            strcmp(users[i].password, password) == 0) {
            current_user_id = users[i].id;
            return 1;
        }
    }
    return 0;
}

static int find_user_by_id(unsigned char user_id) {
    for (int i = 0; i < user_count; i++) {
        if (users[i].id == user_id) {
            return i;
        }
    }
    return -1;
}

static void init(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    
    char password[MAX_PASSWORD_LEN + 1];
    generate_random_string(password, MAX_PASSWORD_LEN);
    password[MAX_PASSWORD_LEN] = '\0';
    
    register_user("admin", password);

    // read flag from file
    FILE *flag = fopen("flag.txt", "r");
    if (flag == NULL) {
        perror("Failed to open flag.txt");
        exit(EXIT_FAILURE);
    }
    fread(secret_vault[0].content, 1, MAX_VAULT_LEN, flag);
    fclose(flag);
}

static int get_user_input(char *buffer, size_t size) {
    if (fgets(buffer, size, stdin) == NULL) {
        return 0;
    }
    
    buffer[strcspn(buffer, "\n")] = '\0';
    return 1;
}

static void show_prompt(void) {
    if (is_logged_in) {
        int user_index = find_user_by_id(current_user_id);
        if (user_index >= 0) {
            printf("%s@vault> ", users[user_index].username);
        } else {
            printf("user@vault> ");
        }
    } else {
        printf("guest@vault> ");
    }
}

static void cmd_register(char *username, char *password) {
    if (is_logged_in) {
        printf("You are already logged in. Logout first to register a new user.\n");
        return;
    }
    
    if (username == NULL || password == NULL) {
        printf("Usage: register <username> <password>\n");
        return;
    }
    
    int result = register_user(username, password);
    if (result == 1) {
        printf("User '%s' registered successfully!\n", username);
    } else if (result == -1) {
        printf("Username '%s' already exists. Please choose a different username.\n", username);
    } else {
        printf("Failed to register user.\n");
    }
}

static void cmd_login(char *username, char *password) {
    if (is_logged_in) {
        printf("You are already logged in. Logout first to login as another user.\n");
        return;
    }
    
    if (username == NULL || password == NULL) {
        printf("Usage: login <username> <password>\n");
        return;
    }
    
    if (authenticate_user(username, password)) {
        printf("Welcome, %s!\n", username);
        is_logged_in = 1;
    } else {
        printf("Invalid username or password.\n");
    }
}

static void cmd_read_vault(void) {
    if (!is_logged_in) {
        printf("You must be logged in to read vault.\n");
        return;
    }
    
    int user_index = find_user_by_id(current_user_id);
    if (user_index >= 0) {
        printf("=== Your Vault ===\n");
        if (strlen(secret_vault[user_index].content) > 0) {
            printf("%s\n", secret_vault[user_index].content);
        } else {
            printf("Your vault is empty.\n");
        }
    } else {
        printf("Invalid user session.\n");
    }
}

static void cmd_write_vault(char *content) {
    if (!is_logged_in) {
        printf("You must be logged in to write to vault.\n");
        return;
    }
    
    if (content == NULL) {
        printf("Usage: write_vault <content>\n");
        return;
    }
    
    int user_index = find_user_by_id(current_user_id);
    if (user_index >= 0) {
        strncpy(secret_vault[user_index].content, content, MAX_VAULT_LEN);
        secret_vault[user_index].content[MAX_VAULT_LEN] = '\0';
        printf("Vault updated successfully!\n");
    } else {
        printf("Invalid user session.\n");
    }
}

static void cmd_logout(void) {
    if (!is_logged_in) {
        printf("You are not logged in.\n");
        return;
    }
    
    int user_index = find_user_by_id(current_user_id);
    if (user_index >= 0) {
        printf("Goodbye, %s!\n", users[user_index].username);
    } else {
        printf("Goodbye!\n");
    }
    is_logged_in = 0;
    current_user_id = -1;
}

static void cmd_help(void) {
    printf("Available commands:\n");
    if (is_logged_in) {
        printf("  read_vault                    - Read your vault content\n");
        printf("  write_vault <content>         - Write content to your vault\n");
        printf("  logout                        - Logout from current session\n");
        printf("  help                          - Show this help message\n");
        printf("  exit                          - Exit the program\n");
    } else {
        printf("  register <username> <password> - Register a new user\n");
        printf("  login <username> <password>    - Login with username and password\n");
        printf("  help                          - Show this help message\n");
        printf("  exit                          - Exit the program\n");
    }
}

static void parse_command(char *input) {
    char *command = strtok(input, " ");
    if (command == NULL) {
        return;
    }
    
    if (strcmp(command, "register") == 0) {
        char *username = strtok(NULL, " ");
        char *password = strtok(NULL, " ");
        cmd_register(username, password);
        
    } else if (strcmp(command, "login") == 0) {
        char *username = strtok(NULL, " ");
        char *password = strtok(NULL, " ");
        cmd_login(username, password);
        
    } else if (strcmp(command, "read_vault") == 0) {
        cmd_read_vault();
        
    } else if (strcmp(command, "write_vault") == 0) {
        char *content = strtok(NULL, "");
        if (content != NULL && content[0] == ' ') {
            content++;
        }
        cmd_write_vault(content);
        
    } else if (strcmp(command, "logout") == 0) {
        cmd_logout();
        
    } else if (strcmp(command, "help") == 0) {
        cmd_help();
        
    } else if (strcmp(command, "exit") == 0) {
        printf("Goodbye!\n");
        exit(EXIT_SUCCESS);
        
    } else {
        printf("Unknown command: %s\n", command);
        printf("Type 'help' for available commands.\n");
    }
}

int main(void) {
    char input[MAX_COMMAND_LEN];
    
    init();
    
    printf("=== Vault System ===\n");
    printf("Type 'help' for available commands.\n");
    
    while (1) {
        show_prompt();
        
        if (!get_user_input(input, sizeof(input))) {
            break;
        }
        
        parse_command(input);
    }
    
    return EXIT_SUCCESS;
}