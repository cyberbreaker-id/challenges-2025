#!/bin/sh
export FLAG=$(cat flag.txt)
socat tcp-l:9101,reuseaddr,fork exec:"./mspaint-000"
