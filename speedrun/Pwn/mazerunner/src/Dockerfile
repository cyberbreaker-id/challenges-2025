FROM ubuntu:24.04@sha256:b59d21599a2b151e23eea5f6602f4af4d7d31c4e236d22bf0b62b86d2e386b8f 

RUN apt update && apt install -y socat

RUN useradd -u 1001 -s /bin/bash ctf

COPY ./mazerunner /home/ctf/
COPY ./run.sh /home/ctf/
COPY ./flag.txt /home/ctf/flag.txt

RUN chown -R root:root /home/ctf/
RUN chmod -R 555 /home/ctf/
USER ctf
WORKDIR /home/ctf/

CMD ["./run.sh"]
