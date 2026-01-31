#!/bin/sh
socat tcp-l:9106,reuseaddr,fork exec:"./mixup"
