#!/usr/bin/env python3
import sys

BANNER = (
    "Sudden Death\n"
)

def main():
    sys.stdout.write(BANNER)
    sys.stdout.write(">>> ")
    sys.stdout.flush()

    code = sys.stdin.readline(256)
    try:
        result = eval(code)
    except Exception as e:
        print("Error.")

if __name__ == "__main__":
    main()
