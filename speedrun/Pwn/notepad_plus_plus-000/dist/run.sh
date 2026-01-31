#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"./notepad_plus_plus-000"
