#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"./ldd-000"
