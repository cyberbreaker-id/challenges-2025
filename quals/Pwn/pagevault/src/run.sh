#!/bin/sh

cd "$(dirname "$0")" || exit 1
if /home/user/pow; then
    exec timeout --foreground 300 qemu-system-x86_64 -m 128M \
	-monitor /dev/null \
	-serial stdio \
	-kernel /home/user/bzImage \
	-initrd /home/user/rootfs.cpio.gz \
	-nographic \
	--append "console=ttyS0 kaslr loglevel=5" \
	-nographic \
	-accel tcg \
	-cpu max,+smap,+smep
else 
    echo "Incorrect POW"
fi

