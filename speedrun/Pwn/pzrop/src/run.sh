#!/bin/sh
socat tcp-l:9111,reuseaddr,fork exec:"./puzzle-rop"
