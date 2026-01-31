#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"script -q -c ./ncursed /dev/null"
