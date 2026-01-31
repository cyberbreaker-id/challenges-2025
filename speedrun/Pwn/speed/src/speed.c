#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ACCOUNT_NAME_LEN 4194304
#define ACCOUNT_PASSWORD_LEN 4194304
#define MAX_NUM_ACCOUNTS 48
#define ADMIN_ACCOUNT_NAME "admin"

#define MAX_LINE_LENGTH 256
#define BRUTEFORCE_TIMEOUT 10

#define ACCOUNTS_FILE "./accounts.txt"

typedef struct AccountInfo {
    char *username;
    char *password;
} AccountInfo;

typedef struct NoDuplicatesValidationInfo {
    char *username;
    size_t newAccountIdx;
} NoDuplicatesValidationInfo;

static AccountInfo *accounts[MAX_NUM_ACCOUNTS];
static size_t numAccounts;

static char *authenticatedAccountName;

static void addAccount(const char *username, const char *password);
static void tryAuthenticate();
static void printAccount(const char *accountName);

static void *verifyNoDuplicatesExist(void *name);

static void initAccounts();
static void userCreateAccount();
static void printLogo();

static void addAccount(const char *username, const char *password) {
    AccountInfo *newAccount = malloc(sizeof(AccountInfo));
    if(!newAccount) {
        fprintf(stderr, "New account malloc failed!\n");
        exit(-1);
    }

    if(strlen(username) >= ACCOUNT_NAME_LEN) {
        fprintf(stderr, "Username too long!\n");
        exit(-1);
    }

    if(strlen(password) >= ACCOUNT_PASSWORD_LEN) {
        fprintf(stderr, "Password too long!\n");
        exit(-1);
    }

    if(numAccounts >= MAX_NUM_ACCOUNTS) {
        fprintf(stderr, "Max number of accounts already exist!\n");
        exit(-1);
    }

    char *accountUsername = malloc(strlen(username) + 1);
    strcpy(accountUsername, username);
    newAccount->username = accountUsername;

    char *accountPassword = malloc(strlen(password) + 1);
    strcpy(accountPassword, password);
    newAccount->password = accountPassword;

    pthread_t *thread = malloc(sizeof(pthread_t));
    NoDuplicatesValidationInfo *validationInfo = malloc(sizeof(NoDuplicatesValidationInfo));
    validationInfo->username = newAccount->username;
    validationInfo->newAccountIdx = numAccounts;

    // async to void making the user wait too long if we have a lot of accounts
    pthread_create(thread, NULL, (void *(*)(void *))verifyNoDuplicatesExist, (void *)validationInfo);

    accounts[numAccounts] = newAccount;
    numAccounts++;
}

static void printAccount(const char *accountName) {
    AccountInfo *account = NULL;
    for(size_t i = 0; i < numAccounts; i++) {
        AccountInfo *tmpAccount = accounts[i];
        if(!strcmp(tmpAccount->username, accountName)) {
            account = tmpAccount;
            break;
        }
    }

    if(!account) {
        printf("ERROR: Trying to print non-existent account\n");
        exit(-1);
    }

    printf("{\n");
    printf("\tUsername: %s,\n", account->username);
    printf("\tPassword: %s,\n", account->password);
    printf("}\n");
}

static void *verifyNoDuplicatesExist(void *voidValidationInfo) {
    NoDuplicatesValidationInfo *validationInfo = (NoDuplicatesValidationInfo *)voidValidationInfo;
    bool conflictingAccount = false;
    for(size_t accountIdx = 0; accountIdx < validationInfo->newAccountIdx; accountIdx++) {
        const char *accountName = accounts[accountIdx]->username;
        const char *tmpName = validationInfo->username;

        bool foundAccount = true;
        while(*accountName || *tmpName) {
            size_t accountNameLength = strlen(accountName);
            size_t tmpNameLength = strlen(tmpName);

            if(accountNameLength || tmpNameLength) {
                if(accountNameLength && tmpNameLength) {
                    if(*accountName != *tmpName) {
                        foundAccount = false; // this account isn't a match
                        break;
                    }
                } else {
                    foundAccount = false;
                }
            }

            if(accountNameLength) {
                accountName++;
            }

            if(tmpNameLength) {
                tmpName++;
            }
        }

        conflictingAccount |= foundAccount;
    }

    if(conflictingAccount) {
        fprintf(stderr, "ERROR: Account already exists: %s\n", validationInfo->username);
        exit(-1);
    }

    return NULL;
}

static void initAccounts() {
    FILE *wordsFile = fopen(ACCOUNTS_FILE, "r");
    if(!wordsFile) {
        fprintf(stderr, "Error opening wordlist file!\n");
        exit(-1);
    }

    char *username = malloc(ACCOUNT_NAME_LEN);
    char *password = malloc(ACCOUNT_PASSWORD_LEN);

    if((!username) || (!password)) {
        fprintf(stderr, "username/password alloc failure\n");
        exit(-1);
    }

    while(fscanf(wordsFile, "%s %s ", username, password) == 2) {
        addAccount(username, password);
    }

    if(!feof(wordsFile)) {
        fprintf(stderr, "Error reading all accounts from wordlist file!\n");
    }
    fclose(wordsFile);

    free(username);
    free(password);
}

static void printLogo() {
    puts("██╗░░░░░██╗███╗░░██╗███████╗");
    puts("██║░░░░░██║████╗░██║╚════██║");
    puts("██║░░░░░██║██╔██╗██║░░███╔═╝");
    puts("██║░░░░░██║██║╚████║██╔══╝░░");
    puts("███████╗██║██║░╚███║███████╗");
    puts("╚══════╝╚═╝╚═╝░░╚══╝╚══════╝");
    printf("\n\n");
}

static void printOptions() {
    if(authenticatedAccountName) {
        printf("Welcome %s! \n", authenticatedAccountName);
    } else {
        printf("Battle Begin! \n");
    }

    printf("\n\n");
    printf("Please select an option below: \n");
    printf("\n\n");

    printf("1. My Logo\n");
    printf("2. Login\n");
    printf("3. Create account\n");
    printf("4. Print current account\n");
    printf("5. Exit\n");
}

static void tryAuthenticate() {
    char *username = malloc(ACCOUNT_NAME_LEN);
    char *password = malloc(ACCOUNT_PASSWORD_LEN);

    if((!username) || (!password)) {
        fprintf(stderr, "username/password alloc failure\n");
        exit(-1);
    }

    printf("Please enter username: ");
    fflush(stdout);
    fgets(username, ACCOUNT_NAME_LEN, stdin);
    username[strlen(username) - 1] = '\0';

    printf("Please enter password for %s: ", username);
    fflush(stdout);
    fgets(password, ACCOUNT_PASSWORD_LEN, stdin);
    password[strlen(password) - 1] = '\0';

    char *authenticationUsername = NULL;
    for(size_t i = 0; i < numAccounts; i++) {
        AccountInfo *account = accounts[i];
        if((!strcmp(account->username, username)) && (!strcmp(account->password, password))) {
            authenticationUsername = account->username;
        }
    }

    if(authenticationUsername) {
        printf("Welcome, %s\n", username);
        authenticatedAccountName = authenticationUsername;
    } else {
        printf("Login failure\n");
        printf("Timeout of %d seconds. No brute forcing allowed!\n", BRUTEFORCE_TIMEOUT);
        authenticatedAccountName = NULL;
    }

    free(username);
    free(password);
}

static void userCreateAccount() {
    char *username = malloc(ACCOUNT_NAME_LEN);
    char *password = malloc(ACCOUNT_PASSWORD_LEN);

    if((!username) || (!password)) {
        fprintf(stderr, "username/password alloc failure\n");
        exit(-1);
    }

    printf("Please enter username: ");
    fflush(stdout);
    fgets(username, ACCOUNT_NAME_LEN, stdin);
    printf("%zd\n", strlen(username));
    username[strlen(username) - 1] = '\0';

    printf("Please enter password: ");
    fflush(stdout);
    fgets(password, ACCOUNT_PASSWORD_LEN, stdin);
    password[strlen(password) - 1] = '\0';

    addAccount(username, password);
    printf("Account created successfully!\n");

    free(username);
    free(password);
}

int main(int argc, char **argv) {
    (void)argc;
    (void)argv;

    // disable input + output buffering
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    initAccounts();

    printLogo();

    int option;
    bool running = true;
    while(running) {
        printOptions();
        printf("\n> ");
        fflush(stdout);
        if(scanf("%d", &option) != 1) {
            printf("Invalid option!\n");
            running = false;
            continue;
        }

        printf("\n\n");

        // Try and get rid of newline.
        char maybeNewline = getc(stdin);
        if(maybeNewline != '\n') {
            ungetc(maybeNewline, stdin);
        }

        switch(option) {
            case 1:
                printLogo();
                break;
            case 2:
                tryAuthenticate();
                break;
            case 3:
                userCreateAccount();
                break;
            case 4:
                if(authenticatedAccountName) {
                    printAccount(authenticatedAccountName);
                    printf("\n");
                } else {
                    fprintf(stderr, "ERROR: You need to log in first!\n\n");
                }
                break;
            case 5:
                printf("Goodbye!\n");
                running = false;
                break;
            default:
                printf("Invalid option!\n");
                running = false;
                break;
        }
    }
}