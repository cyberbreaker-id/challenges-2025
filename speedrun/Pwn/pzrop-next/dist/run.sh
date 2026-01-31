#!/bin/sh
socat tcp-l:9113,reuseaddr,fork exec:"./puzzle-rop"
