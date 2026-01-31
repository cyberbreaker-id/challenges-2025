FROM python:3.9-alpine

RUN apk update && apk add socat

RUN adduser -D -u 1001 -s /bin/bash ctf

COPY ./lz1 /home/ctf/
COPY ./run.py /home/ctf/
COPY ./run.sh /home/ctf/
COPY ./flag.txt /home/ctf/

RUN chown -R root:root /home/ctf/
RUN chmod -R 555 /home/ctf/
USER ctf
WORKDIR /home/ctf/

CMD ["./run.sh"]
