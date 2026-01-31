#!/bin/sh

qemu-system-x86_64 -m 128M \
	-monitor /dev/null \
	-serial stdio \
	-kernel ./bzImage \
	-initrd ./rootfs.cpio.gz \
	-nographic \
	--append "console=ttyS0 kaslr loglevel=5" \
	-nographic \
	-accel tcg \
	-cpu max,+smap,+smep
