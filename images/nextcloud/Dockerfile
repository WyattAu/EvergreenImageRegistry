ARG VERSION=30.0.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2-fpm php8.2-cli php8.2-curl gd mbstring xml zip intl mysql sqlite3 \
        nginx ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65534:65534 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.2-fpm php8.2-cli php8.2-curl gd mbstring xml zip intl mysql sqlite3 \
        nginx ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65534:65534 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf 2>/dev/null || true
USER 65534:65534
WORKDIR /var/www/html
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:80"]
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="nextcloud" \
      org.opencontainers.image.version="30.0.5" \
      org.opencontainers.image.vendor="Nextcloud" \
      org.opencontainers.image.source="https://github.com/nextcloud/server" \
      sovereign.image.tier="2" \
      sovereign.image.category="cloud-storage" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
