FROM php:8.2-apache

USER root

# RUN apt update && apt install sqlite3

COPY ./flag.txt /flag.txt

RUN chown -R www-data:www-data /var/www
USER www-data

COPY --chown=www-data:www-data ./src /var/www
