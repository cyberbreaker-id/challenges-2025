#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"python3 run.py"
