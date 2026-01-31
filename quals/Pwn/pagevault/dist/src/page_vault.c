#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/mm.h> // For page allocation functions

#define DEVICE_NAME "page_vault"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("CTF Designer");

struct vault_session {
    struct page *vault_page;
};

// --- IOCTL Definitions ---
#define VAULT_ALLOC _IO('k', 1)
#define VAULT_FREE  _IO('k', 2)
#define VAULT_EDIT  _IOW('k', 3, char*)
#define VAULT_READ  _IOR('k', 4, char*)


static int page_vault_open(struct inode *inode, struct file *filp) {
    struct vault_session *session = kzalloc(sizeof(*session), GFP_KERNEL);
    if (!session) {
        return -ENOMEM;
    }
    filp->private_data = session;
    printk(KERN_INFO "page_vault: New session started.\n");
    return 0;
}

static int page_vault_release(struct inode *inode, struct file *filp) {
    struct vault_session *session = filp->private_data;
    if (session->vault_page) {
        printk(KERN_INFO "page_vault: Leaked page detected! Freeing on close.\n");
        __free_page(session->vault_page);
    }
    kfree(session);
    printk(KERN_INFO "page_vault: Session ended.\n");
    return 0;
}

static long page_vault_ioctl(struct file *filp, unsigned int cmd, unsigned long arg) {
    struct vault_session *session = filp->private_data;
    char *page_vaddr;

    switch (cmd) {
        case VAULT_ALLOC:
            if (session->vault_page) return -EBUSY;
            session->vault_page = alloc_page(GFP_KERNEL);
            if (!session->vault_page) return -ENOMEM;
            printk(KERN_INFO "page_vault: Page allocated.\n");
            return 0;

        case VAULT_FREE:
            if (!session->vault_page) return -EINVAL;
            __free_page(session->vault_page);
            printk(KERN_INFO "page_vault: Page freed.\n");
            return 0;

        case VAULT_EDIT:
            if (!session->vault_page) return -EINVAL;
            page_vaddr = page_address(session->vault_page);
            if (!page_vaddr) return -EFAULT;
            if (copy_from_user(page_vaddr, (void __user *)arg, 0x1000)) {
                return -EFAULT;
            }
            printk(KERN_INFO "page_vault: Page edited.\n");
            return 0;
        
        case VAULT_READ:
            if (!session->vault_page) return -EINVAL;
            page_vaddr = page_address(session->vault_page);
            if (!page_vaddr) return -EFAULT;
            if (copy_to_user((void __user *)arg, page_vaddr, 0x1000)) {
                return -EFAULT;
            }
            printk(KERN_INFO "page_vault: Page read.\n");
            return 0;

        default:
            return -EINVAL;
    }
}

static const struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = page_vault_open,
    .release = page_vault_release,
    .unlocked_ioctl = page_vault_ioctl,
};

static struct miscdevice dev;

static int dev_init(void) {
	dev.minor = MISC_DYNAMIC_MINOR;
	dev.name = DEVICE_NAME;
	dev.fops = &fops;
	dev.mode = 0644;

	if (misc_register(&dev)) {
		return -1;
	}


	return 0;
}

static void dev_cleanup(void) {
	misc_deregister(&dev);
}


module_init(dev_init);
module_exit(dev_cleanup);
