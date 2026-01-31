import sys

def xor_with_words(data: bytearray, keys: list[str]) -> bytearray:
    for word in keys:
        key_bytes = word.encode()  # konversi kata ke bytes
        for i in range(len(data)):
            data[i] ^= key_bytes[i % len(key_bytes)]
    return data

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 encoder.py <input_flag.txt> <keys.txt> <output_flag.enc>")
        sys.exit(1)

    flag_path, keys_path, out_path = sys.argv[1:4]

    with open(flag_path, "rb") as f:
        data = bytearray(f.read().strip())

    with open(keys_path, "r", encoding="utf-8") as f:
        keys = [line.strip() for line in f if line.strip()]

    enc = xor_with_words(data, keys)

    with open(out_path, "wb") as f:
        f.write(enc)

if __name__ == "__main__":
    main()

