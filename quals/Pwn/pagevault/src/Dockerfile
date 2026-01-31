FROM ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30

RUN apt-get update -y && \
    apt-get install -y lib32z1 socat --no-install-recommends && \
    apt-get install qemu-system -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m user

COPY bzImage /home/user/
COPY rootfs.cpio.gz /home/user/
COPY pow /home/user/
COPY run.sh /
COPY start_service.sh /

WORKDIR /home/user

RUN chmod +x pow && \
    chmod +x /run.sh && \
    chmod +x /start_service.sh

EXPOSE 9102

CMD ["/start_service.sh"]
