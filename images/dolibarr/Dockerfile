ARG VERSION=23.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php84-fpm php84 php84-curl php84-gd php84-mbstring php84-xml zip php84-intl php84-mysql openssl php84-pdo json-c soap \
        nginx ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-gd php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-mysql openssl php-8.4-pdo json-c nginx ca-certificates
RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443
ENTRYPOINT ["php-fpm8.2"]
LABEL org.opencontainers.image.title="dolibarr" \
      org.opencontainers.image.version="23.0.2" \
      org.opencontainers.image.vendor="Dolibarr" \
      org.opencontainers.image.source="https://github.com/Dolibarr/dolibarr" \
      sovereign.image.tier="2" \
      sovereign.image.category="crm-erp" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM