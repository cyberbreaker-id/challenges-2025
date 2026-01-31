#!/bin/bash

cd "$(dirname "$0")" || exit 1
socat TCP-LISTEN:9102,fork,reuseaddr EXEC:./run.sh,stderr
