KDIR ?= /opt/linux/src/linux-6.12.38
PWD := $(shell pwd)

obj-m := page_vault.o

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
