#!/bin/sh
socat tcp-l:9103,reuseaddr,fork exec:"/home/ctf/early"