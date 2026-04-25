ARG VERSION=2.4.14
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        php8.4-fpm php84 php8.4-curl php8.4-mbstring php8.4-xml zip php8.4-intl php8.4-mysql openssl php8.4-pdo \
        nginx ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-8.4 php-8.4-curl php-8.4-mbstring php-8.4-xml zip php-8.4-intl php-8.4-pdo_mysql php-8.4-mysqli openssl php-8.4-pdo nginx ca-certificates
RUN mkdir -p /var/run/php /var/www/html /var/log/nginx /var/cache/nginx \
    && chown -R 65532:65532 /var/www/html /var/log/nginx /var/cache/nginx /var/run/php
COPY --from=builder /etc/nginx/nginx.conf /etc/nginx/nginx.conf
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443
ENTRYPOINT ["php-fpm8.4"]
LABEL org.opencontainers.image.title="frontaccounting" \
      org.opencontainers.image.version="2.4.14" \
      org.opencontainers.image.vendor="FrontAccounting" \
      org.opencontainers.image.source="https://sourceforge.net/projects/frontaccounting/" \
      sovereign.image.tier="2" \
      sovereign.image.category="business-finance" \
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