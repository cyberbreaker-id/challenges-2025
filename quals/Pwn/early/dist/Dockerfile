FROM ubuntu:24.04

RUN apt update -y
RUN apt install python3 socat adduser -y

RUN adduser --disabled-password --uid 1001 --shell /bin/bash ctf

COPY ./early /home/ctf/
COPY ./run.sh /home/ctf/
COPY ./flag.txt /home/ctf/

RUN chown -R root:root /home/ctf/
RUN chmod -R 555 /home/ctf/
USER ctf
WORKDIR /home/ctf/

CMD ["./run.sh"]