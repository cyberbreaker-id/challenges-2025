#!/bin/sh

# Start MariaDB in background
mariadbd-safe --datadir=/var/lib/mysql &

# Wait for MariaDB to be ready
echo "Waiting for MariaDB to start..."
sleep 15

# Wait for MariaDB to be fully ready
while ! mariadb -h localhost -e "SELECT 1" >/dev/null 2>&1; do
    echo "Waiting for MariaDB connection..."
    sleep 2
done

# Create database and set root password
mariadb -h localhost -e "CREATE DATABASE IF NOT EXISTS secure_notes;"
mariadb -h localhost -e "SET PASSWORD FOR root@localhost = PASSWORD('example');"

echo "MariaDB setup complete"

# Stop MariaDB
pkill mariadbd
sleep 5

# Start all services with supervisor
supervisord -c /etc/supervisor/conf.d/supervisord.conf