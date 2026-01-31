#!/usr/bin/env python3

import subprocess
import base64
import tempfile
import sys
import os

try:
    mode = input("(c)ompress or (d)ecompress: ")
    mode = mode.strip()
    if mode == 'c':
        pointer_length = int(input("Pointer length: "))
        if not 0 <= pointer_length <= 15:
            raise Exception("Invalid pointer length")
        data = input("Enter data to compress base64 encoded: ")
        with tempfile.NamedTemporaryFile() as input_file, tempfile.NamedTemporaryFile() as output_file:
            input_file.write(base64.b64decode(data))
            input_file.flush()
            subprocess.check_call(["./lz1", "c", str(pointer_length), input_file.name, output_file.name], stdin=None, stdout=None, stderr=None)
    elif mode == 'd':
        data = input("Enter data to decompress base64 encoded: ")
        with tempfile.NamedTemporaryFile() as input_file, tempfile.NamedTemporaryFile() as output_file:
            input_file.write(base64.b64decode(data))
            input_file.flush()
            subprocess.check_call(["./lz1", "d", input_file.name, output_file.name], stdin=None, stdout=None, stderr=None)
    else:
        raise Exception("Invalid mode")
except Exception as e:
    print(e)



