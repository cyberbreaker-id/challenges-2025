# Build with NASM + GCC linker. Produces: puzzle-rop (static addresses, NX stack)

BIN := puzzle-rop
ASM := puzzle_rop.asm
OBJ := $(ASM:.asm=.o)

all: $(BIN)

$(OBJ): $(ASM)
	nasm -felf64 -g -F dwarf $< -o $@

$(BIN): $(OBJ)
	# -no-pie for fixed code addresses, -z noexecstack enforces NX stack
	gcc -nostartfiles -no-pie -z noexecstack -o $@ $^

clean:
	rm -f $(OBJ) $(BIN)

.PHONY: all clean
