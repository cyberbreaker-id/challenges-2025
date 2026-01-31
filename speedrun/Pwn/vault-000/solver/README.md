# TLDR

Integer overflow on user id which have unsigned char (1 byte) but user register could have > 256 id.

```
typedef struct {
    unsigned char id;
    char username[MAX_USERNAME_LEN + 1];
    char password[MAX_PASSWORD_LEN + 1];
} User;
```

## Solver

Register with > 256 users, user id will reseted into 0 then next user will have same id as admin. Then just login and read the vault to get the flag.
