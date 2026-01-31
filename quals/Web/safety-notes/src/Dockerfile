# Multi-stage build for consolidated services
FROM node:current-alpine as node-build

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN apk add --no-cache chromium \
    nss \
    curl \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont && \
    adduser -h /bot -D puppeteer

# Copy package.json first for npm cache
COPY bot/package*.json /bot/
WORKDIR /bot
RUN npm ci --only=production

COPY bot/ /bot/

# Final stage - combine everything
FROM php:8.2-cli

# Install apt packages in cache-friendly way
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y \
    git \
    apache2 \
    supervisor \
    curl \
    nodejs \
    npm \
    chromium \
    unzip

# Enable Apache modules
RUN a2enmod rewrite proxy proxy_http

# Copy PHP app
COPY app/ /app/
WORKDIR /app

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer install --no-dev --optimize-autoloader

# Copy Node.js bot with dependencies
COPY --from=node-build /bot /bot

# Copy Apache configuration
COPY conf/apache2-debian.conf /etc/apache2/apache2.conf

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    APP_URL=http://localhost/

EXPOSE 80 

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]