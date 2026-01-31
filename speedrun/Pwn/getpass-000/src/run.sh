#!/bin/sh
socat tcp-l:9101,reuseaddr,fork exec:"./getpass-000"
