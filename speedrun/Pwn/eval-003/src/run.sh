#!/bin/sh
socat tcp-l:9112,reuseaddr,fork exec:"./eval-003"
