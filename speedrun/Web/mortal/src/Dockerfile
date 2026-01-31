FROM caddy:2-alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY html/ /srv/

EXPOSE 80

COPY flag.txt /flag.txt
RUN mv /flag.txt /flag-$(cat /dev/urandom|head -n 512|md5sum|cut -c1-32).txt

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]