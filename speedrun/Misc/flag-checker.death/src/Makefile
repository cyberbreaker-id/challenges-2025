# Makefile for flag challenge

CC = gcc
CFLAGS = -O0 -fno-stack-protector -no-pie
TARGET = flag
SRC = flag.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
