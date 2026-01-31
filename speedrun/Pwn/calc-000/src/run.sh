#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"./calc-000"
