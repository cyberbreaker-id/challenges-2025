#include <stdio.h>
#include <string.h>
#include <stdint.h>

int check_flag(const char *input) {
    // Encoded version of the flag (each byte XORed with 0x55)
    uint8_t encoded_flag[] = {0x16, 0x11, 0x16, 0x2e, 0x30, 0x34, 0x26, 0x3c, 0x30, 0x26, 0x21, 0x0a, 0x27, 0x30, 0x23, 0x0a, 0x36, 0x3d, 0x34, 0x39, 0x39, 0x30, 0x3b, 0x32, 0x30, 0x0a, 0x34, 0x31, 0x66, 0x64, 0x33, 0x65, 0x28};
    size_t len = sizeof(encoded_flag);

    // Compare input length
    if (strlen(input) != len) return 0;

    // XOR check
    for (size_t i = 0; i < len; i++) {
        if ((input[i] ^ 0x55) != encoded_flag[i])
            return 0;
    }
    return 1;
}

int main() {
    char buf[64];  // buffer large enough for the flag
    printf("Enter the flag: ");

    // Read input safely
    if (!fgets(buf, sizeof(buf), stdin)) {
        printf("Input error!\n");
        return 1;
    }

    // Remove newline if present
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n')
        buf[len-1] = '\0';

    if (check_flag(buf)) {
        printf("Correct! Flag unlocked.\n");
    } else {
        printf("Wrong!\n");
    }

    return 0;
}

