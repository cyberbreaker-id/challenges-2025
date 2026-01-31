FROM php:8.2-apache

ENV APACHE_DOCUMENT_ROOT=/var/www/html

COPY ./src /var/www/html
COPY flag.txt /flag.txt

RUN FILENAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12).txt && \
    mv /flag.txt /$FILENAME && \
    chmod 444 /$FILENAME

RUN find /var/www/html -type d -exec chmod 555 {} \; && \
    find /var/www/html -type f -exec chmod 444 {} \;

EXPOSE 80
