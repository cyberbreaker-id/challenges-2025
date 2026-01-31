# Build stage for app dependencies
FROM node:current-alpine AS app-builder
WORKDIR /app
COPY app/package*.json ./
RUN npm ci --only=production

# Build stage for bot dependencies  
FROM node:current-alpine AS bot-builder
WORKDIR /bot
COPY bot/package*.json ./
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
RUN npm ci --only=production

# Final runtime stage
FROM node:current-alpine AS runtime

# Cache APK packages
RUN --mount=type=cache,target=/var/cache/apk \
    apk update && apk add --no-cache \
    mariadb \
    mariadb-client \
    chromium \
    nss \
    curl \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    supervisor \
    nginx \
    bash

# Create directories
RUN mkdir -p /app /bot /var/log/supervisor

# Copy app files and dependencies
COPY app/ /app/
COPY --from=app-builder /app/node_modules /app/node_modules

# Copy bot files and dependencies
COPY bot/ /bot/
COPY --from=bot-builder /bot/node_modules /bot/node_modules

# Create MariaDB user and directories
RUN mkdir -p /run/mysqld && \
    chown -R mysql:mysql /run/mysqld /var/lib/mysql

# Initialize MariaDB
RUN mariadb-install-db --user=mysql --datadir=/var/lib/mysql

# Copy configuration files
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose ports
EXPOSE 80

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

ENV ADMIN_USERNAME="admin" \
    ADMIN_PASSWORD="8da6da8d986cdd201f74216ad8c7dc2c51e6a26d74677d419c7ae90b0abc2d3d" \
    SECRET_KEY="6931914f4ba74cefbe0b34c1bb591eb289874a860507ec0ff606727fe87670ae" \
    DB_HOST="localhost" \
    DB_PORT="3306" \
    DB_USER="root" \
    DB_PASSWORD="example" \
    DB_NAME="secure_notes" \
    APP_URL="http://localhost/"

WORKDIR /app

# Start all services
CMD ["/docker-entrypoint.sh"]
